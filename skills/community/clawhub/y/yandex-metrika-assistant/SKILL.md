---
name: yandex-metrika-assistant
description: OpenClaw + Яндекс.Метрика API — stat/Logs/management, OAuth, presets, UTM, цели, CSV, квоты; плагин yandex-metrika-assistant.
homepage: https://github.com/Horosheff/yandex-metrika-assistant
---

# Яндекс.Метрика API — заточка под **OpenClaw**

Плагин: **`yandex-metrika-assistant`** (`openclaw.plugin.json` в этой папке).  
Цель: ноль сюрпризов — сначала **конфиг и секреты**, потом **правильный endpoint**, без выдуманных метрик и без утечки токена.

---

## Онбординг человека (порядок ответов агента)

**Если токена ещё нет** (пользователь только ставит навык или не настроил ключ):

1. **Сначала** дай ссылку и краткое резюме установки: **`{baseDir}/docs/INSTALL-FOR-HUMANS-RU.md`** (шаги OpenClaw + OAuth + куда вставить ключ).
2. **Обязательно** перечисли, какие **галочки в приложении Яндекс OAuth** нужны для Метрики (таблица из того же файла / шаг 2): статистика и чтение, создание/изменение счётчиков, при необходимости расходы, параметры пользователей, офлайн-данные.
3. Укажи **канал поддержки:** [**https://t.me/maya_pro**](https://t.me/maya_pro) — вопросы по установке и сценариям; **не** проси кидать токен в Telegram публично.
4. Затем — получение токена: **`{baseDir}/docs/INSTRUCTION-GET-TOKEN-RU.md`** (или ссылка `authorize` с `oauthClientId` из конфига).
5. Напомни: ключ хранить в **`oauthToken`** плагина или в **`YANDEX_METRIKA_OAUTH_TOKEN`**, не в чате.

**После того как ключ добавлен** (пользователь сообщил, что сохранил токен в конфиг, или токен уже есть в конфиге/окружении):

- Не проси продиктовать токен.
- Заверши ответ блоком **«С чего начать»** — предложи **3–5 коротких вариантов** (нумерованный список), например:
  1. Показать список счётчиков Метрики.  
  2. Визиты по дням за последние 7 дней.  
  3. Сводка по источникам трафика.  
  4. Топ страниц по просмотрам.  
  5. Конверсии по цели (если есть цели).  

Полный список идей — **`{baseDir}/docs/INSTALL-FOR-HUMANS-RU.md`** (раздел «После добавления ключа») и **`{baseDir}/docs/10-user-intents-matrix.md`**.

---

**Типовые формулировки пользователей** («откуда трафик», «цели», «UTM», «география», «сравни периоды», «выгрузи CSV», «сырые логи») — смотри матрицу: **`{baseDir}/docs/10-user-intents-matrix.md`** (разбивка по разделам A–J + ссылки на официальные примеры и пресеты).

---

## OpenCLaw: порядок работы (строго)

1. **Токен** брать только из:
   - настроек плагина **`oauthToken`** (см. `configSchema` в `openclaw.plugin.json`), **или**
   - переменной окружения **`YANDEX_METRIKA_OAUTH_TOKEN`** (если хост OpenClaw так настроен), **или**
   - пользователь явно передал токен **один раз** для текущей сессии — тогда использовать, но **не** повторять токен обратно в ответе и **не** вставлять в файлы репозитория.
2. Если токена **нет** — **не** вызывать API и **не** придумывать ответ Метрики. Следуй разделу **«Онбординг человека»** выше: сначала **`{baseDir}/docs/INSTALL-FOR-HUMANS-RU.md`**, галочки OAuth, [**@maya_pro**](https://t.me/maya_pro), затем **`{baseDir}/docs/INSTRUCTION-GET-TOKEN-RU.md`**; при наличии **`oauthClientId`** — ссылка `authorize?response_type=token&client_id=...`.
3. **`defaultCounterId`** из конфига: если пользователь не назвал счётчик — используй это значение и **одной строкой** напиши: «использую счётчик по умолчанию из конфига OpenClaw».
4. Любые `curl`/команды в чат — только с плейсхолдером **`$env:YANDEX_METRIKA_OAUTH_TOKEN`** или «подставь токен из секрета OpenClaw», **не** вставляй токен целиком.
5. **Windows / PowerShell:** если `curl -H "Authorization: OAuth …"` даёт ошибки из‑за кавычек — используй **`Invoke-RestMethod`** с `-Headers @{ Authorization = 'OAuth ' + $env:YANDEX_METRIKA_OAUTH_TOKEN }`** или заголовок через **конкатенацию** в скобках: `-H ('Authorization: OAuth ' + $env:YANDEX_METRIKA_OAUTH_TOKEN)`. Подробно: **`{baseDir}/docs/OPENCLAW-AGENT.md`**, **`{baseDir}/docs/EXAMPLES.md`**.

---

## Быстрые рецепты (копипаста для пользователя, Windows PowerShell)

Подстановка токена из env (удобно рядом с OpenClaw):

```powershell
$env:YANDEX_METRIKA_OAUTH_TOKEN = "<секрет, не коммитить>"
$cid = "<COUNTER_ID>"
# Надёжнее без вложенных кавычек вокруг токена:
curl.exe -s -H ('Authorization: OAuth ' + $env:YANDEX_METRIKA_OAUTH_TOKEN) `
  "https://api-metrika.yandex.net/management/v1/counters?per_page=20"
```

Отчёт «визиты за последние 7 дней» (проверь `ids` и метрики по задаче):

```powershell
curl.exe -s -G "https://api-metrika.yandex.net/stat/v1/data" `
  --data-urlencode "ids=$cid" `
  --data-urlencode "metrics=ym:s:visits" `
  --data-urlencode "date1=7daysAgo" `
  --data-urlencode "date2=yesterday" `
  -H ('Authorization: OAuth ' + $env:YANDEX_METRIKA_OAUTH_TOKEN)
```

---

## Сценарий: «пришли ежедневную статистику по сайту maya»

Так OpenClaw **должен** отработать запрос (и что увидит человек в ответе).

### Внутренние шаги агента

1. **Токен** — из `oauthToken` / `YANDEX_METRIKA_OAUTH_TOKEN`. Нет токена → стоп, ссылка на `{baseDir}/docs/INSTRUCTION-GET-TOKEN-RU.md`.
2. **Счётчик** — если в конфиге есть **`defaultCounterId`** и пользователь не просил другой сайт, можно спросить: «использовать счётчик по умолчанию?» или сразу использовать, если контекст однозначен.
3. Иначе: **`GET /management/v1/counters`** с **`search_string=maya`** (или фрагмент домена: `mayai`, `blog.mayai`). Если **несколько** счётчиков — перечислить `id`, `name`, `site` и **попросить выбрать** один `id`.
4. **Период** — если не сказан, предложить по умолчанию, например **вчера − 29 дней … вчера** (без «сегодня» для стабильности данных) или уточнить у пользователя.
5. **Ежедневная разбивка** — API отчётов:
   - вариант А: `GET .../stat/v1/data` с группировкой по дню визита **`dimensions=ym:s:date`**, **`metrics`** по задаче (часто `ym:s:visits`, при необходимости `ym:s:pageviews`, `ym:s:users` — имена проверять в [справочнике](https://yandex.ru/dev/metrika/ru/stat/));
   - вариант Б: `GET .../stat/v1/data/bytime` — если удобнее именно «по времени» (см. openapi в доке stat).
6. Вызвать API (или дать пользователю **одну** готовую команду с плейсхолдерами), распарсить JSON.
7. Если в ответе **`contains_sensitive_data": true`** — кратко предупредить про ограничение раскрытия данных.

### Как выглядит ответ человеку (шаблон)

Агент пишет **короткое резюме**, затем **таблицу или список по дням** (дата → визиты / просмотры / и т.д.), без сырого JSON на экран целиком, если пользователь не просил сырой вывод.

Пример формулировки:

- «Счётчик: **LAYMI** (`id` …), сайт **blog.mayai.ru**, период **…**. Ниже визиты по дням. Данные из API Метрики, токен из конфига OpenClaw.»
- Далее строки вида: `2025-03-01 — визиты: 120`, …
- Примечание при 429: «Сработала квота отчётов; повтори через несколько минут» (`{baseDir}/docs/04-quotas.md`).

### Пример цепочки запросов (PowerShell, без секрета в логах чата)

```powershell
# 1) Найти счётчик по подстроке (maya / mayai)
curl.exe -s -G "https://api-metrika.yandex.net/management/v1/counters" `
  --data-urlencode "search_string=maya" `
  --data-urlencode "per_page=50" `
  -H ('Authorization: OAuth ' + $env:YANDEX_METRIKA_OAUTH_TOKEN)

# 2) Ежедневные визиты (подставь $cid из шага 1)
curl.exe -s -G "https://api-metrika.yandex.net/stat/v1/data" `
  --data-urlencode "ids=$cid" `
  --data-urlencode "dimensions=ym:s:date" `
  --data-urlencode "metrics=ym:s:visits" `
  --data-urlencode "date1=30daysAgo" `
  --data-urlencode "date2=yesterday" `
  --data-urlencode "sort=ym:s:date" `
  -H ('Authorization: OAuth ' + $env:YANDEX_METRIKA_OAUTH_TOKEN)
```

Точные **`metrics`/`dimensions`** при спорных отчётах — только из официальной доки, не по памяти модели.

---

## Сценарий: «на какую страницу больше трафика?»

Запрос про **страницы** — это снова **API отчётов** `GET .../stat/v1/data`, после того же **разрешения счётчика** (id / `defaultCounterId` / `search_string`), что и в сценарии выше.

### Смысл «трафика»

- Чаще всего пользователь имеет в виду **просмотры страниц** (хиты): группировка по URL страницы + метрика просмотров. Тогда в одном запросе используется **только префикс `ym:pv:`** (визиты и хиты в основном наборе не смешивать).
- Если нужны **входы / визиты с первой страницы** (лендинги), это другой отчёт: группировки уровня **визита** (`ym:s:...`), другие метрики — уточнить у пользователя или дать оба коротко («по просмотрам лидирует …, по визитам на входе …»), опираясь на [справочник группировок](https://yandex.ru/dev/metrika/ru/stat/).

### Типовой запрос (топ URL по просмотрам)

Параметры (имена перепроверять в доке при смене версии API):

- `dimensions` — URL страницы на уровне хита, например **`ym:pv:URL`**.
- `metrics` — **`ym:pv:pageviews`** (и при необходимости ещё метрики из того же множества `ym:pv:`).
- `sort` — по убыванию просмотров, в доке Метрики для сортировки по убыванию часто используется **`-`** перед метрикой (см. `{baseDir}/docs/05-reports-api-stat.md`).
- `limit` — топ **10–20** URL, чтобы ответ был читаемым.
- `date1` / `date2` — как в других сценариях (если не заданы — default или вопрос пользователю).

### Как выглядит ответ человеку

Коротко: период, счётчик, что считали (**просмотры по URL**). Затем список: **URL → число просмотров** (топ N). Длинные URL можно обрезать визуально с «…», полный URL — по наведению или второй строкой при необходимости.

### Пример `curl` (PowerShell)

```powershell
curl.exe -s -G "https://api-metrika.yandex.net/stat/v1/data" `
  --data-urlencode "ids=$cid" `
  --data-urlencode "dimensions=ym:pv:URL" `
  --data-urlencode "metrics=ym:pv:pageviews" `
  --data-urlencode "sort=-ym:pv:pageviews" `
  --data-urlencode "limit=15" `
  --data-urlencode "date1=30daysAgo" `
  --data-urlencode "date2=yesterday" `
  -H ('Authorization: OAuth ' + $env:YANDEX_METRIKA_OAUTH_TOKEN)
```

Если API вернёт ошибку совместимости группировки и метрики — не «угадывать» замену, а свериться с актуальным openapi для `/stat/v1/data` на сайте Метрики.

---

## Маршрутизация: что дергать

| Запрос пользователя | Куда | Файл |
|---------------------|------|------|
| Отчёт, метрики, период, сегменты | `GET .../stat/v1/data` (и др. из stat) | `{baseDir}/docs/05-reports-api-stat.md` |
| Топ страниц, «куда больше трафика» | `stat/v1/data`, группировка URL (`ym:pv:`) | сценарий ниже, `{baseDir}/docs/05-reports-api-stat.md` |
| Сырые логи, выгрузка | `management/v1/counter/{id}/logrequests...` | `{baseDir}/docs/06-logs-api.md` |
| Список счётчиков, цели, настройки | `management/v1/...` | `{baseDir}/docs/08-management-quickstart.md` |
| Загрузка расходов, CRM, офлайн | data-import | `{baseDir}/docs/07-data-import.md` |
| 401/403, scope | OAuth | `{baseDir}/docs/03-auth-oauth.md`, `{baseDir}/docs/INSTRUCTION-GET-TOKEN-RU.md` |
| 429 | Квоты | `{baseDir}/docs/04-quotas.md` |
| «Что ещё спрашивают / не знаю какой отчёт» | Матрица намерений | `{baseDir}/docs/10-user-intents-matrix.md` |

Смешанная задача: **сначала** `counters` или `defaultCounterId`, **потом** stat/logs.

---

## Железные правила API

- Заголовок: **`Authorization: OAuth <access_token>`** (слово `OAuth` и пробел обязательны).
- Хост: **`https://api-metrika.yandex.net`**
- В одном запросе **stat** не смешивать **`ym:s:`** и **`ym:pv:`** в основных `metrics`/`dimensions` (детали в `{baseDir}/docs/05-reports-api-stat.md`).
- Лимиты: до **20** метрик, **10** группировок в `/stat/v1/data`; **200 запросов / 5 мин** на этот endpoint на пользователя; Logs с IP — **10**/с.
- Имена метрик/группировок **не выдумывать** — только из официального справочника (ссылки в `{baseDir}/docs/01-links-and-hub.md`).
- После скачивания Logs — **`clean`**, квота хранилища **10 ГБ** на счётчик (`{baseDir}/docs/06-logs-api.md`).

---

## Формат ответа агента OpenClaw

1. Что сделано / что предлагается (1 фраза).  
2. Откуда взяты токен и счётчик (конфиг / env / спросил у пользователя).  
3. Команда или URL-шаблон **без секрета**.  
4. Как проверить успех (HTTP 200, поля JSON).  
5. Риски: квоты, `contains_sensitive_data`, 429.

---

## Карта файлов

| Файл | Назначение |
|------|------------|
| `openclaw.plugin.json` | Контракт OpenClaw: `oauthToken`, `defaultCounterId`, `oauthClientId` |
| `{baseDir}/docs/INSTALL-FOR-HUMANS-RU.md` | Установка: OpenClaw, OAuth-галочки, TG, после ключа — с чего начать |
| `{baseDir}/docs/INSTRUCTION-GET-TOKEN-RU.md` | Токен для людей |
| `{baseDir}/docs/OPENCLAW-AGENT.md` | Установка: нет HOOK.md; PowerShell без ловушек кавычек |
| GitHub: `Horosheff/yandex-metrika-assistant` → `scripts/exchange-yandex-oauth-code.ps1` | Обмен `code` → token (в этом пакете не включён) |
| `{baseDir}/docs/01`–`09` | Справка по разделам API |
| `{baseDir}/docs/10-user-intents-matrix.md` | **Матрица вопросов пользователей → API** (ресёрч по примерам и пресетам) |

Официальный хаб: https://yandex.ru/dev/metrika
