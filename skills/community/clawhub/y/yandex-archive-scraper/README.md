# yandex-archive-scraper

A powerful skill for searching and extracting data from Yandex.Archive (Яндекс.Архив) using `Scrapling` to bypass bot protection and Cloudflare Turnstile.

## Features
- Converts natural language queries into optimized Yandex.Archive search URLs.
- Uses `Scrapling` (StealthyFetcher) to bypass Yandex bot protection.
- Extracts search results (document titles, text snippets, and direct links).
- Supports pagination to collect multiple pages of results.
- Can search across all three Yandex.Archive indexes:
  - `archive` (Архивы) — Metric books, revision tales, confessional statements.
  - `mass_media` (Периодика) — Old newspapers (e.g., "Senate Gazette", "Provincial Gazette").
  - `directories` (Справочники) — Address calendars, lists of residents, memorable books.

## Installation

1. Install the required dependencies:
```bash
pip install scrapling playwright curl_cffi patchright msgspec browserforge
playwright install chromium
```

2. Add the skill to your agent.

## Usage

Run the script directly from the command line:
```bash
python search.py "Александр Пушкин" archive 2
```

Or use it as an agent tool:
```json
{
  "name": "yandex_archive_search",
  "arguments": {
    "query": "Александр Пушкин Москва",
    "index": "archive",
    "max_pages": 2
  }
}
```

---

# yandex-archive-scraper (Русский)

Мощный скилл для поиска и извлечения данных из Яндекс.Архива с использованием фреймворка `Scrapling` для обхода защиты от ботов и Cloudflare Turnstile.

## Возможности
- Преобразует запросы на естественном языке в оптимизированные URL для поиска по Яндекс.Архиву.
- Использует `Scrapling` (StealthyFetcher) для обхода защиты Яндекса.
- Извлекает результаты поиска (названия документов, текстовые фрагменты/сниппеты и прямые ссылки).
- Поддерживает пагинацию для сбора нескольких страниц результатов.
- Умеет искать по всем трем базам Яндекс.Архива:
  - `archive` (Архивы) — Метрические книги, ревизские сказки, исповедные ведомости.
  - `mass_media` (Периодика) — Старые газеты (например, "Сенатские ведомости", "Губернские ведомости").
  - `directories` (Справочники) — Адрес-календари, списки жителей, памятные книжки.

## Установка

1. Установите необходимые зависимости:
```bash
pip install scrapling playwright curl_cffi patchright msgspec browserforge
playwright install chromium
```

2. Добавьте скилл в вашего агента.

## Использование

Запуск скрипта напрямую из командной строки:
```bash
python search.py "Александр Пушкин" archive 2
```

Или использование в качестве инструмента агента:
```json
{
  "name": "yandex_archive_search",
  "arguments": {
    "query": "Александр Пушкин Москва",
    "index": "archive",
    "max_pages": 2
  }
}
```