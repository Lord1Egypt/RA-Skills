---
name: yandex-archive-scraper
description: Search and extract data from Yandex.Archive (Яндекс.Архив) — metric books, newspapers, directories. Bypasses bot protection via Scrapling.
---

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

## Tools

### `yandex_archive_search`
Search Yandex.Archive based on a natural language query.
**Parameters:**
- `query` (string): The search query (e.g., "Александр Пушкин Москва").
- `index` (string, optional): The index to search in. Options: `archive` (default), `mass_media`, `directories`.
- `max_pages` (integer, optional): Maximum number of pages to scrape (default 1).

## Requirements
- `scrapling`
- `playwright`
- `curl_cffi`
- `patchright`
- `msgspec`
- `browserforge`

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

## Инструменты (Tools)

### `yandex_archive_search`
Поиск по Яндекс.Архиву на основе текстового запроса.
**Параметры:**
- `query` (string): Поисковый запрос (например, "Александр Пушкин Москва").
- `index` (string, optional): Раздел для поиска. Варианты: `archive` (по умолчанию), `mass_media`, `directories`.
- `max_pages` (integer, optional): Максимальное количество страниц для парсинга (по умолчанию 1).

## Зависимости
- `scrapling`
- `playwright`
- `curl_cffi`
- `patchright`
- `msgspec`
- `browserforge`