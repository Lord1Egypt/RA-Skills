#!/usr/bin/env python3
import io
import json
import sys
from app.config import AppConfig
from core.orchestrator import Orchestrator


def make_json_safe(value):
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, list):
        return [make_json_safe(v) for v in value]
    if isinstance(value, dict):
        return {k: make_json_safe(v) for k, v in value.items()}
    if hasattr(value, '__dict__'):
        return {k: make_json_safe(v) for k, v in value.__dict__.items()}
    return str(value)


def _configure_stdout_utf8():
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        return
    except Exception:
        pass

    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass


def _dependency_warnings(runner: Orchestrator):
    warnings = []
    if getattr(runner.config.runtime, 'use_dom_backend', False) and not runner.browser.dom.is_available():
        warnings.append(
            "DOM backend 未就绪：将回退到视觉点击。若需浏览器 DOM 自动化，请安装 playwright，并确保 bridges/playwright_dom_bridge.py 可运行。"
        )
    if not getattr(runner.vision.ocr, 'available', False):
        warnings.append(
            "OCR 未就绪：未检测到 pytesseract，文本按钮/输入框识别能力会下降。可执行：pip install pytesseract，并安装 Tesseract OCR。"
        )
    return warnings


def main():
    _configure_stdout_utf8()

    if len(sys.argv) < 2:
        print("用法: python main.py '命令'")
        return 1

    command = sys.argv[1]
    runner = Orchestrator(AppConfig())
    result = runner.execute(command)
    payload = make_json_safe(result)
    payload["warnings"] = _dependency_warnings(runner)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if result.get('success') else 2


if __name__ == '__main__':
    raise SystemExit(main())
