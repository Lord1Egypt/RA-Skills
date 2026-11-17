#!/usr/bin/env python3
"""Проверка (и опционально установка) окружения для пайплайна саммари/перевода PDF.

    python3 install_libraries.py            # только проверка импортов
    python3 install_libraries.py --install  # доустановить пакеты, затем проверить

Коды возврата: 0 — всё на месте, 1 — есть несобранные импорты (см. строки FAIL).
Скрипт не выбрасывает traceback наружу: любой сбой печатается как строка отчёта.
"""

import subprocess
import sys

PACKAGES = [
    "pymupdf",
    "pillow",
    "PyPDF2",
    "pdf2image",
    # langchain строго 1.x: create_agent и ToolCallLimitMiddleware появились в нём
    "langchain>=1.0",
    "langchain-core",
    "langchain-deepseek",
    "langchain-openai",
    "beautifulsoup4",
    "lxml",
    "pandas",
    "rich",
    "python-dotenv",
    "nest_asyncio",
    "aiofiles",
    "tqdm",
    "loguru",
    "playwright",
    "weasyprint",
    "pypdf",
    "paddlepaddle==3.0.0",
    "paddleocr>=3.0",
]

# Каждый пункт: (метка для отчёта, исполняемый код импорта).
CHECKS = [
    ("pymupdf", "import pymupdf"),
    ("pillow", "from PIL import Image"),
    ("PyPDF2", "import PyPDF2"),
    ("pdf2image", "from pdf2image import convert_from_path"),
    ("langchain.tools", "from langchain.tools import tool"),
    ("langchain_core.tools", "from langchain_core.tools import BaseTool, tool"),
    ("langchain.agents.create_agent", "from langchain.agents import create_agent"),
    ("langchain.agents.middleware",
     "from langchain.agents.middleware import ToolCallLimitMiddleware"),
    ("langchain_core.messages",
     "from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage"),
    ("langchain_core.prompts",
     "from langchain_core.prompts import ChatPromptTemplate, PromptTemplate"),
    ("langchain_deepseek", "from langchain_deepseek import ChatDeepSeek"),
    ("langchain_openai", "from langchain_openai import ChatOpenAI"),
    ("bs4", "from bs4 import BeautifulSoup"),
    ("pandas", "import pandas as pd"),
    ("rich", "from rich import print as pprint"),
    ("dotenv", "from dotenv import load_dotenv; load_dotenv()"),
    ("nest_asyncio", "import nest_asyncio"),
    ("aiofiles", "import aiofiles"),
    ("tqdm", "from tqdm import tqdm"),
    ("loguru", "from loguru import logger as loguru_logger"),
    ("paddle", "import paddle; paddle.set_device('cpu')"),
    ("paddleocr.PPStructureV3", "from paddleocr import PPStructureV3"),
    ("paddlex.ImageWriter",
     "from paddlex.inference.utils.io.writers import ImageWriter"),
]

# Модули самого проекта, а не пакеты PyPI. Вне каталога проекта их
# отсутствие ожидаемо и ошибкой не считается.
PROJECT_MODULES = [
    ("html_to_pdf_summary", "from html_to_pdf_summary import html_to_pdf"),
    ("html2pdf_latest", "from html2pdf_latest import html_to_pdf"),
    ("merge_html_latest", "from merge_html_latest import merge_html_folder"),
]


def run(cmd, what):
    """Запустить подпроцесс, вернуть True/False и напечатать понятный итог."""
    try:
        proc = subprocess.run(cmd)
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"FAIL {what}: не удалось запустить — {exc}", flush=True)
        return False
    if proc.returncode != 0:
        print(f"FAIL {what}: код возврата {proc.returncode}", flush=True)
        return False
    print(f"OK   {what}", flush=True)
    return True


def install():
    if sys.version_info[:2] != (3, 11):
        print(f"WARN Python {sys.version_info.major}.{sys.version_info.minor}, "
              f"ожидается 3.11 — у paddlepaddle==3.0.0 может не быть колёс",
              flush=True)
    pip = [sys.executable, "-m", "pip", "install"]
    # cryptography ставим готовым колесом до paddleocr: иначе она собирается
    # из исходников и падает на отсутствующем Rust-тулчейне.
    run(pip + ["--only-binary=:all:", "cryptography"], "cryptography (wheel)")
    ok = run(pip + PACKAGES, "pip install основных пакетов")
    if not ok:
        print("WARN основной pip install не завершился успешно — "
              "проверка ниже покажет, чего именно не хватает", flush=True)
    run([sys.executable, "-m", "playwright", "install", "chromium"],
        "playwright chromium")


def check():
    print(f"Python {sys.version}", flush=True)
    failed = []
    for label, code in CHECKS:
        try:
            exec(code, {})
        except Exception as exc:
            print(f"FAIL {label}: {type(exc).__name__}: {exc}", flush=True)
            failed.append(label)
        else:
            print(f"OK   {label}", flush=True)

    for label, code in PROJECT_MODULES:
        try:
            exec(code, {})
        except ImportError:
            print(f"SKIP {label}: модуль проекта, вне каталога проекта это норма",
                  flush=True)
        except Exception as exc:
            print(f"SKIP {label}: {type(exc).__name__}: {exc}", flush=True)
        else:
            print(f"OK   {label}", flush=True)
    return failed


def main():
    import os
    import warnings

    warnings.filterwarnings("ignore")
    # Отключаем ускорители paddle, несовместимые с CPU-режимом пайплайна.
    os.environ["FLAGS_use_mkldnn"] = "0"
    os.environ["FLAGS_use_cinn"] = "0"

    if "--install" in sys.argv:
        install()

    failed = check()
    if failed:
        print(f"\nне собралось импортов: {len(failed)} — {', '.join(failed)}")
        print("повторите запуск с флагом --install")
        return 1
    print("libraries installation complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
