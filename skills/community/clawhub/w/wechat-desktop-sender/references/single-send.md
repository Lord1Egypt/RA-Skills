# Single Send

## Install

```bash
pip install pywinauto pyperclip psutil pywin32 pillow pytesseract
```

If OCR verification is needed, also install local Tesseract OCR and ensure `tesseract.exe` is in PATH.

## Command

```bash
python scripts/wechat_send.py --to "文件传输助手" --message "你好"
```

## Main flags

- `--to` target chat name
- `--message` message body
- `--delay` wait after each UI step
- `--log-dir` custom log directory
- `--dump-tree` dump WeChat control tree for debugging
- `--verify-title` check current window title
- `--ocr-verify` run OCR verification after send
- `--no-screenshot` disable failure screenshot

## Debug examples

```bash
python scripts/wechat_send.py --to "文件传输助手" --message "调试测试" --dump-tree --verify-title
python scripts/wechat_send.py --to "文件传输助手" --message "OCR测试" --ocr-verify
```
