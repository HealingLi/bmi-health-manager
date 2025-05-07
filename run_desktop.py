import threading
import webview
from app import app

def run_flask():
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # 打开桌面窗口
    webview.create_window('BMI健康管理系统', 'http://127.0.0.1:5000/') 