# Заметки для агента OpenClaw (установка и тест)

## HOOK.md не нужен

В корне репозитория есть **`openclaw.plugin.json`** — это **нативный плагин** OpenClaw с вложенным навыком (`"skills": ["."]` → тот же каталог с **`SKILL.md`**).

- **Hook** — отдельный тип расширения; для этого проекта файл **`HOOK.md` не предусмотрен** и **не обязателен**.
- Если установщик ищет только hook — ставьте артефакт как **skill** (`openclaw skills install …`) **или** как **плагин** (`openclaw plugins install <path>`) и включайте плагин в `plugins.entries`.

## Тест API без «проблем с кавычками» (Windows PowerShell)

`curl.exe` с длинным заголовком `Authorization` в нескольких строках с **обратными кавычками** часто ломается из‑за вложенных `"` или «умных» кавычек из мессенджера.

**Предпочтительно для проверки:** `Invoke-RestMethod` и хештаблица заголовков (токен только из переменной окружения или секрета, **не** вставлять токен в чат в команду целиком).

```powershell
$env:YANDEX_METRIKA_OAUTH_TOKEN = '<ВСТАВИТЬ_ТОЛЬКО_ЛОКАЛЬНО_ИЗ_СЕКРЕТА>'
$h = @{ Authorization = 'OAuth ' + $env:YANDEX_METRIKA_OAUTH_TOKEN }
Invoke-RestMethod -Uri 'https://api-metrika.yandex.net/management/v1/counters?per_page=5' -Headers $h
```

Одинарные кавычки `'...'` вокруг URI снижают риск, что PowerShell что‑то подставит лишнее.

## Однострочный curl (если нужен именно curl)

```powershell
curl.exe -s -H ('Authorization: OAuth ' + $env:YANDEX_METRIKA_OAUTH_TOKEN) "https://api-metrika.yandex.net/management/v1/counters?per_page=5"
```

Здесь заголовок собран через **конкатенацию**, без вложенных двойных кавычек вокруг токена.

## Токен

- Не просить пользователя присылать токен в открытый чат; если прислали — **не повторять** токен в ответе и посоветовать **перевыпустить** в [oauth.yandex.ru](https://oauth.yandex.ru/).
- В OpenClaw: `plugins.entries.yandex-metrika-assistant.config.oauthToken` или `skills.entries` / секреты хоста — см. [`SKILL.md`](../SKILL.md).

Больше примеров: [`EXAMPLES.md`](./EXAMPLES.md).
