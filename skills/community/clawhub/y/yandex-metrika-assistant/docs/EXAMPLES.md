# Примеры запросов к API (ручные и для отладки)

Перед вызовами нужны **OAuth-токен** и **id счётчика**. Токен не вставляйте в публичные репозитории и чаты.

Удобно задать переменную окружения:

```powershell
$env:YANDEX_METRIKA_OAUTH_TOKEN = "<ваш_токен>"
$cid = "99223440"   # подставьте свой counter id
```

Заголовок для всех запросов к `api-metrika.yandex.net`:

```http
Authorization: OAuth <access_token>
```

### PowerShell: если «ломаются кавычки» с curl

Не вставляйте токен из чата в середину строки с кавычками. Задайте **`$env:YANDEX_METRIKA_OAUTH_TOKEN`** отдельно (из секрета), затем:

```powershell
$h = @{ Authorization = 'OAuth ' + $env:YANDEX_METRIKA_OAUTH_TOKEN }
Invoke-RestMethod -Uri 'https://api-metrika.yandex.net/management/v1/counters?per_page=10' -Headers $h
```

Или одна строка **curl** без вложенных кавычек вокруг токена:

```powershell
curl.exe -s -H ('Authorization: OAuth ' + $env:YANDEX_METRIKA_OAUTH_TOKEN) 'https://api-metrika.yandex.net/management/v1/counters?per_page=10'
```

Для агента OpenClaw: см. также [`OPENCLAW-AGENT.md`](./OPENCLAW-AGENT.md).

---

## 1. Список доступных счётчиков

```powershell
curl.exe -s -G "https://api-metrika.yandex.net/management/v1/counters" `
  --data-urlencode "per_page=50" `
  -H "Authorization: OAuth $env:YANDEX_METRIKA_OAUTH_TOKEN" | ConvertFrom-Json | Select-Object -ExpandProperty counters | Format-Table id, name, site
```

Поиск по подстроке (название или домен):

```powershell
curl.exe -s -G "https://api-metrika.yandex.net/management/v1/counters" `
  --data-urlencode "search_string=blog" `
  --data-urlencode "per_page=20" `
  -H "Authorization: OAuth $env:YANDEX_METRIKA_OAUTH_TOKEN"
```

---

## 2. Визиты по дням за последние 30 дней

```powershell
curl.exe -s -G "https://api-metrika.yandex.net/stat/v1/data" `
  --data-urlencode "ids=$cid" `
  --data-urlencode "dimensions=ym:s:date" `
  --data-urlencode "metrics=ym:s:visits" `
  --data-urlencode "date1=30daysAgo" `
  --data-urlencode "date2=yesterday" `
  --data-urlencode "sort=ym:s:date" `
  -H "Authorization: OAuth $env:YANDEX_METRIKA_OAUTH_TOKEN"
```

---

## 3. Топ страниц по просмотрам (хиты)

В одном запросе используется только префикс **`ym:pv:`**.

```powershell
curl.exe -s -G "https://api-metrika.yandex.net/stat/v1/data" `
  --data-urlencode "ids=$cid" `
  --data-urlencode "dimensions=ym:pv:URL" `
  --data-urlencode "metrics=ym:pv:pageviews" `
  --data-urlencode "sort=-ym:pv:pageviews" `
  --data-urlencode "limit=15" `
  --data-urlencode "date1=30daysAgo" `
  --data-urlencode "date2=yesterday" `
  -H "Authorization: OAuth $env:YANDEX_METRIKA_OAUTH_TOKEN"
```

---

## 4. Отчёт по шаблону (preset) — «источники, сводка»

```powershell
curl.exe -s -G "https://api-metrika.yandex.net/stat/v1/data" `
  --data-urlencode "ids=$cid" `
  --data-urlencode "preset=sources_summary" `
  --data-urlencode "date1=7daysAgo" `
  --data-urlencode "date2=yesterday" `
  -H "Authorization: OAuth $env:YANDEX_METRIKA_OAUTH_TOKEN"
```

Другие пресеты: [шаблоны в доке Метрики](https://yandex.ru/dev/metrika/ru/stat/presets).

---

## 5. Выгрузка в CSV

Добавьте суффикс **`.csv`** к пути метода:

```
https://api-metrika.yandex.net/stat/v1/data.csv?ids=...&metrics=...&dimensions=...
```

---

## 6. Обмен кода OAuth на токен (authorization code)

Скрипт в репозитории: [`exchange-yandex-oauth-code.ps1`](https://github.com/Horosheff/yandex-metrika-assistant/blob/main/scripts/exchange-yandex-oauth-code.ps1).

Пошаговая выдача токена в браузере: [`INSTRUCTION-GET-TOKEN-RU.md`](./INSTRUCTION-GET-TOKEN-RU.md).

---

## Ограничения

- Квоты: см. [`docs/04-quotas.md`](./04-quotas.md).
- Имена метрик и группировок — только из [официального справочника](https://yandex.ru/dev/metrika/ru/stat/).
