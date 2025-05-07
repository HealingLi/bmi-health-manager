# BMI健康管理系统

一个支持多用户注册、登录、BMI记录与历史查询的健康管理软件，支持网页端和桌面端（Mac/Windows/Linux）。未来可扩展为安卓App。

## 功能

- 多用户注册/登录
- 记录和查询个人BMI历史
- 健康建议提醒
- 桌面版（PyWebview）
- 支持打包为本地可执行文件

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行网页版

```bash
python app.py
```

浏览器访问 http://127.0.0.1:5000/

### 3. 运行桌面版

```bash
pip install pywebview
python run_desktop.py
```

### 4. 打包为桌面应用（以Mac为例）

```bash
pyinstaller --noconfirm --onefile --windowed --add-data "templates:templates" run_desktop.py
```

打包产物在 `dist/` 目录下。

## 目录结构

- `app.py`：主后端逻辑
- `run_desktop.py`：桌面版启动脚本
- `templates/`：前端页面模板
- `requirements.txt`：依赖列表
- `.gitignore`：Git忽略文件

## 常见问题

### 1. 打包后模板找不到？

请确保打包命令包含 `--add-data "templates:templates"`，并已按文档修改 `app.py` 的 Flask 初始化部分。

### 2. Mac 下无法打开可执行文件？

请在"系统设置-隐私与安全-开发者工具"中允许，或用 `chmod +x dist/run_desktop` 赋予权限。

### 3. 依赖安装失败？

请确保使用 Python 3.8+，并激活虚拟环境。

## 打包和分发说明

- 推荐用 PyInstaller 打包，详见上文命令。
- 分发时无需包含 `.venv/`、`build/`、`dist/`、`*.db` 等文件。
- 可将 `dist/run_desktop` 直接发给其他用户。

## API接口预告

未来将支持 RESTful API，方便安卓/小程序等多端接入。

## 许可证

MIT License

---

GitHub 用户名：HealingLi
