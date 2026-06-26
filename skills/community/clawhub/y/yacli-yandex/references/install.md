# Installation

## English

This skill does not vendor `yacli` itself. It assumes the operator installs and configures `yacli` plus `mcporter` on their own OpenClaw host.

### Upstream project
- `yacli`: `https://github.com/NextStat/yacli`

### Minimum setup
1. Install `mcporter`
2. Install `yacli`
3. Make sure `yacli-mcp-server` is available on the host
4. Add a `yacli` entry to the active `mcporter.json`
5. Authenticate at least one Yandex account for the services you plan to use
6. Start a fresh OpenClaw session so the skill is discoverable

### Bundled helpers
- `scripts/install-yacli.sh` — validates the expected host-side prerequisites and prints the next steps
- `scripts/check-yacli.sh` — checks MCP schema plus account/auth visibility
- `assets/mcporter.yacli.example.json` — machine-readable example `mcporter` entry

### What the operator should verify
- `mcporter list yacli --schema --config <path-to-mcporter.json>`
- `mcporter call --server yacli --tool yacli.account.list --args '{}' --config <path-to-mcporter.json>`
- `mcporter call --server yacli --tool yacli.auth.status --args '{}' --config <path-to-mcporter.json>`

### Important note about mcporter syntax
- For this MCP server, use `--server` and `--tool` when the tool name itself contains dots
- Example:
  - `mcporter call --server yacli --tool yacli.mail.folders --args '{}' --config <path-to-mcporter.json>`
- Avoid forms like `mcporter call yacli.mail.folders ...`, because some runtimes split that selector at the first dot and incorrectly call `mail`

### If `yacli` is missing
- Follow the upstream installation instructions from the `yacli` repository
- If you package `yacli` differently in your environment, that is fine as long as the MCP server entry resolves to a working `yacli-mcp-server`

## Русский

Этот skill не включает `yacli` внутрь себя. Предполагается, что оператор отдельно ставит и настраивает `yacli` и `mcporter` на своём OpenClaw host.

### Upstream project
- `yacli`: `https://github.com/NextStat/yacli`

### Минимальная настройка
1. Установить `mcporter`
2. Установить `yacli`
3. Убедиться, что `yacli-mcp-server` доступен на хосте
4. Добавить `yacli` в активный `mcporter.json`
5. Авторизовать хотя бы один Яндекс-аккаунт для нужных сервисов
6. Запустить новую сессию OpenClaw, чтобы skill был подхвачен

### Вспомогательные файлы в bundle
- `scripts/install-yacli.sh` — проверяет базовые зависимости и подсказывает следующие шаги
- `scripts/check-yacli.sh` — проверяет MCP schema, список аккаунтов и auth status
- `assets/mcporter.yacli.example.json` — пример записи для `mcporter.json`

### Что оператору нужно проверить
- `mcporter list yacli --schema --config <path-to-mcporter.json>`
- `mcporter call --server yacli --tool yacli.account.list --args '{}' --config <path-to-mcporter.json>`
- `mcporter call --server yacli --tool yacli.auth.status --args '{}' --config <path-to-mcporter.json>`

### Важная заметка про синтаксис mcporter
- Для этого MCP server используйте `--server` и `--tool`, если имя tool само содержит точки
- Пример:
  - `mcporter call --server yacli --tool yacli.mail.folders --args '{}' --config <path-to-mcporter.json>`
- Избегайте формы `mcporter call yacli.mail.folders ...`, потому что некоторые runtime режут такой selector по первой точке и ошибочно вызывают `mail`

### Если `yacli` ещё не установлен
- Следуйте upstream-инструкциям из репозитория `yacli`
- Если в вашей среде `yacli` упакован иначе, это нормально, если MCP entry всё равно указывает на рабочий `yacli-mcp-server`
