# PyAutoGUI Controller - Refactor MVP

这是第一版重构落地：

- 统一核心类型：`ParsedIntent` / `TaskStep` / `DetectedElement` / `ExecutionResult`
- 重写自然语言解析：支持复合命令、目标抽取、位置提示、置信度
- 重写视觉层：`OCR + CV` 混合，统一候选融合排序
- 重写输入层：鼠标/键盘走可验证动作闭环
- 重写调度器：统一 `Orchestrator`
- 保留旧文件，新的主入口为 `main.py` / `app/main.py`

## 目录

```text
app/
core/
nlu/
perception/
action/
runtime/
```

## 运行

```bash
python main.py "打开浏览器访问 https://example.com"
python main.py "点击发送按钮"
python main.py "在搜索框输入 'hello world'"
```

## 当前默认行为

- Windows 终端输出默认按 UTF-8 处理，避免中文 JSON 输出报错
- 浏览器场景默认启用 DOM backend（可通过环境变量关闭）
- 若 DOM/OCR 未就绪，结果 JSON 会返回 `warnings`

关闭 DOM backend：

```bash
set PYAUTOGUI_CONTROLLER_USE_DOM=0
```

## 依赖建议

基础依赖：

```bash
pip install pyautogui pyperclip pillow opencv-python
```

OCR 增强：

```bash
pip install pytesseract
```

> 另外需要系统安装 Tesseract OCR 本体，否则仅安装 `pytesseract` 仍无法真正 OCR。

浏览器 DOM 增强：

```bash
pip install playwright
playwright install chromium
```

如果安装了 `opencv-python` 和 `pytesseract`，视觉识别精度会明显提升；如果安装了 `playwright`，浏览器自动化会优先走 DOM 路径，稳定性更高。
