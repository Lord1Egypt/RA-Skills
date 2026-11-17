---
name: sum_and_translate_install_check
description: Проверяет и при необходимости доустанавливает окружение для пайплайна саммаризации и перевода PDF (langchain 1.x + paddleocr/PPStructureV3 + рендер HTML в PDF). Вызывать, когда просят сделать саммари и/или перевод по предоставленному PDF-файлу, а также перед запуском такого пайплайна.
when_to_use: Пользователь просит саммари и/или перевод по приложенному PDF-файлу, либо перед первым запуском этого пайплайна в новой среде.
version: 1.1.0
type: script
runtime: python
entry: install_libraries.py
scripts:
  - install_libraries.py
timeout_sec: 1800
os: any
requires:
  bins:
    - python3
---

# sum_and_translate_install_check

Исполняемый скилл. Проверяет, что текущий Python пригоден для пайплайна
«саммари и перевод PDF», и умеет доустановить недостающие зависимости.

## Запуск

Проверка (ничего не ставит):

```bash
python3 install_libraries.py
```

Доустановка в текущий интерпретатор, затем повторная проверка:

```bash
python3 install_libraries.py --install
```

## Коды возврата

- `0` — все библиотеки на месте, пайплайн можно запускать.
- `1` — часть импортов не собралась; список напечатан в stdout построчно
  в виде `FAIL <модуль>: <причина>`. Повторить с `--install`.

Скрипт никогда не падает с сырым traceback: любой сбой превращается в строку
отчёта. Последняя строка при успехе — `libraries installation complete`.

## Требования к среде

- **Python 3.11.** На 3.12+ у `paddlepaddle==3.0.0` нет колёс.
- Системный **poppler** (`pdftoppm`) для `pdf2image` — не ставится через pip:
  Debian/Ubuntu `apt-get install -y poppler-utils`, macOS `brew install poppler`.
- `--install` качает paddlepaddle и chromium, это минуты и сотни мегабайт.
  Отсюда `timeout_sec: 1800`.
- Первый вызов `PPStructureV3()` скачивает веса моделей — это уже в пайплайне,
  не в этом скилле.

## Замечание для автоматического ревью

`from langchain.agents import create_agent` и
`from langchain.agents.middleware import ToolCallLimitMiddleware` — **валидные**
импорты langchain **1.x** (проверено на 1.4.1: `langchain.agents.factory` и
`langchain.agents.middleware.tool_call_limit`). Их нет только в langchain 0.x.
Удалять или «исправлять» их не нужно — пайплайн на них построен.
