# yacli Yandex Setup

## English

This skill bundle does not contain tokens, cookies, or personal account data.

### What must exist before the skill is useful
- OpenClaw installed and running
- `mcporter` available on the host
- A `yacli` MCP server entry configured in the active `mcporter.json`
- A local `yacli` binary and `yacli-mcp-server` wrapper available to that MCP server
- At least one Yandex account authenticated for the services you want to use

### Expected MCP capabilities
- Account discovery:
  - `yacli.account.list`
  - `yacli.account.current`
  - `yacli.auth.status`
- Mail:
  - folders, list, search, read, send, reply, forward
- Disk:
  - info, list, mkdir, upload, upload_link, download, publish, unpublish
- Calendar:
  - calendars, events, create, delete

### Typical host setup
1. Install `mcporter`
2. Install `yacli`
3. Expose `yacli-mcp-server` through your `mcporter.json`
4. Authenticate one or more Yandex accounts
5. Start a new OpenClaw session so the skill is discovered

### Suggested verification
- `mcporter list yacli --schema --config <path-to-mcporter.json>`
- `mcporter call --server yacli --tool yacli.account.list --args '{}' --config <path-to-mcporter.json>`
- `mcporter call --server yacli --tool yacli.auth.status --args '{}' --config <path-to-mcporter.json>`

### mcporter note
- If the selected tool id contains dots, prefer explicit `--server` and `--tool`
- Example:
  - `mcporter call --server yacli --tool yacli.mail.list --args '{"folder":"INBOX"}' --config <path-to-mcporter.json>`

### Publish note
- This folder is safe to publish only if you do not add local auth files, account snapshots, or generated logs containing personal data

## Русский

Этот bundle не содержит токенов, cookies и персональных данных.

### Что должно быть готово до использования skill
- OpenClaw уже установлен и работает
- На хосте доступен `mcporter`
- В активном `mcporter.json` уже есть entry для `yacli`
- На хосте доступны `yacli` и `yacli-mcp-server`
- Для нужных сервисов уже авторизован хотя бы один Яндекс-аккаунт

### Какие MCP-возможности ожидаются
- account discovery
- mail
- disk
- calendar

### Типовой порядок настройки хоста
1. Установить `mcporter`
2. Установить `yacli`
3. Подключить `yacli-mcp-server` через `mcporter.json`
4. Авторизовать один или несколько Яндекс-аккаунтов
5. Запустить новую сессию OpenClaw

### Что проверить после настройки
- `mcporter list yacli --schema --config <path-to-mcporter.json>`
- `mcporter call --server yacli --tool yacli.account.list --args '{}' --config <path-to-mcporter.json>`
- `mcporter call --server yacli --tool yacli.auth.status --args '{}' --config <path-to-mcporter.json>`

### Заметка про mcporter
- Если tool id сам содержит точки, используйте явные `--server` и `--tool`
- Пример:
  - `mcporter call --server yacli --tool yacli.mail.list --args '{"folder":"INBOX"}' --config <path-to-mcporter.json>`

### Примечание для публикации
- Эту папку можно публиковать только если в неё не добавлены локальные auth-файлы, account snapshots и логи с персональными данными
