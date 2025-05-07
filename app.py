from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os
import sys

if getattr(sys, 'frozen', False):
    # PyInstaller 打包后的临时目录
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static') if os.path.exists(os.path.join(sys._MEIPASS, 'static')) else None
else:
    template_folder = 'templates'
    static_folder = 'static' if os.path.exists('static') else None

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bmi_users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    bmis = db.relationship('BMIRecord', backref='user', lazy=True)

class BMIRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('用户名已存在')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('邮箱已注册')
            return redirect(url_for('register'))
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('注册成功，请登录')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('用户名或密码错误')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        bmi = weight / (height ** 2)
        record = BMIRecord(height=height, weight=weight, bmi=bmi, user_id=current_user.id)
        db.session.add(record)
        db.session.commit()
        flash(f'您的BMI为 {bmi:.2f}，{bmi_advice(bmi)}')
    records = BMIRecord.query.filter_by(user_id=current_user.id).order_by(BMIRecord.date.desc()).all()
    return render_template('dashboard.html', records=records)

def bmi_advice(bmi):
    if bmi < 18.5:
        return '体重过轻，请注意营养均衡。'
    elif 18.5 <= bmi < 24.9:
        return '体重正常，继续保持！'
    elif 24.9 <= bmi < 28:
        return '超重，请适当锻炼。'
    else:
        return '肥胖，请注意健康饮食和锻炼。'

if __name__ == '__main__':
    if not os.path.exists('bmi_users.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True) 