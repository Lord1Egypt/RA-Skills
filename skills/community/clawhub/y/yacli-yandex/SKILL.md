---
name: yacli-yandex
description: Yandex Mail, Disk, and Calendar via yacli MCP. Работает с Яндекс Почтой, Диском и Календарём: разбор входящих, поиск и чтение писем, ответы, загрузка и публикация файлов, просмотр и планирование событий.
homepage: https://github.com/NextStat/yacli
metadata: {"openclaw":{"emoji":"📮","requires":{"bins":["mcporter"]}}}
triggers:
  - yacli
  - yandex mail
  - yandex disk
  - yandex calendar
  - почта яндекс
  - яндекс диск
  - календарь яндекс
---

# yacli Yandex

## English

Use the `yacli` MCP server for Yandex Mail, Disk, and Calendar workflows.

### Summary
- Use this skill for Yandex Mail, Disk, and Calendar through `yacli`
- It supports inbox triage, search and read flows, replies, Disk uploads and sharing, and calendar lookup or scheduling
- It requires a working `yacli` MCP server and at least one authenticated Yandex account

### Prerequisites
- A working `yacli` MCP server must already be configured in OpenClaw
- At least one Yandex account must already be authenticated for the services you want to use
- If `yacli` is not installed or wired yet, read [references/install.md](references/install.md) and [references/mcporter-config.md](references/mcporter-config.md)
- If tools are missing or auth is incomplete, read [references/setup.md](references/setup.md)

### Account selection
- If the user specifies an account alias or email, use it
- Otherwise start with `yacli.account.current`
- If no current account is set, call `yacli.account.list`
- Before claiming auth is broken, call `yacli.auth.status`

### Critical tool naming rule
- Use concrete MCP tool ids only:
  - `yacli.account.current`
  - `yacli.mail.list`
  - `yacli.disk.upload`
  - `yacli.calendar.events`
- Do not call generic categories such as `mail`, `disk`, `calendar`, `goal.route`, or bare `yacli`
- If you are calling tools through `mcporter` CLI, dotted tool names must be passed with:
  - `mcporter call --server yacli --tool yacli.mail.list --args '{"folder":"INBOX"}'`
- Do not use selector syntax like `mcporter call yacli.mail.list ...` for this server, because some runtimes split at the first dot and end up calling unsupported tools like `mail`

### Mail
1. `yacli.mail.folders`
2. `yacli.mail.list` or `yacli.mail.search`
3. `yacli.mail.read`
4. Then only if needed:
   - `yacli.mail.reply`
   - `yacli.mail.forward`
   - `yacli.mail.send`

### Attachments and invites
- `yacli.mail.attachment.export` to save an attachment on the MCP host
- `yacli.mail.invite.inspect` to parse a calendar invite before acting on it
- `yacli.mail.invite.create_event` only after explicit user approval

### Disk
1. `yacli.disk.info` or `yacli.disk.list`
2. `yacli.disk.mkdir` if a target directory is needed
3. Then one of:
   - `yacli.disk.upload` for a private upload
   - `yacli.disk.upload_link` for upload plus immediate public link
   - `yacli.disk.publish` or `yacli.disk.unpublish` for existing files
   - `yacli.disk.download` to export a private file to the MCP host
4. Use `yacli.mail.send_link` or `yacli.mail.send_published_link` when the user wants a shared file sent by email

### Calendar
1. `yacli.calendar.calendars`
2. `yacli.calendar.events`
3. Then only if needed:
   - `yacli.calendar.create`
   - `yacli.calendar.delete`
- Use an explicit calendar id for writes
- Do not assume a default calendar if listing is available

### Safety rules
- Do not send email without explicit user confirmation of recipients and content unless the user explicitly asked to send it now
- Do not publish private files or create public links without explicit user approval
- Do not create or delete calendar events without explicit user approval
- For destructive or externally visible actions, prefer read/list first, summarize the intended action, then execute

## Русский

Используйте `yacli` MCP server для работы с Яндекс Почтой, Диском и Календарём.

### Кратко
- Используйте этот skill для Яндекс Почты, Диска и Календаря через `yacli`
- Он подходит для разбора входящих, поиска и чтения писем, ответов, загрузки файлов на Диск, публикации ссылок и работы с календарём
- Для работы нужен настроенный `yacli` MCP server и хотя бы один авторизованный Яндекс-аккаунт

### Предпосылки
- В OpenClaw уже должен быть настроен рабочий `yacli` MCP server
- Для нужных сервисов должен быть авторизован хотя бы один Яндекс-аккаунт
- Если `yacli` ещё не установлен или не подключён, смотрите [references/install.md](references/install.md) и [references/mcporter-config.md](references/mcporter-config.md)
- Если tools не видны или auth выглядит сломанным, смотрите [references/setup.md](references/setup.md)

### Выбор аккаунта
- Если пользователь указал alias или email, используйте его
- Иначе начните с `yacli.account.current`
- Если current account не задан, вызовите `yacli.account.list`
- Перед тем как говорить, что auth сломан, вызовите `yacli.auth.status`

### Критичное правило именования tool
- Используйте только конкретные MCP tool id:
  - `yacli.account.current`
  - `yacli.mail.list`
  - `yacli.disk.upload`
  - `yacli.calendar.events`
- Не вызывайте абстрактные категории вроде `mail`, `disk`, `calendar`, `goal.route` или голый `yacli`
- Если вызываете tools через `mcporter` CLI, tool names с точками нужно передавать так:
  - `mcporter call --server yacli --tool yacli.mail.list --args '{"folder":"INBOX"}'`
- Не используйте форму `mcporter call yacli.mail.list ...` для этого сервера, потому что некоторые runtime режут selector по первой точке и в итоге пытаются вызвать неподдерживаемый tool `mail`

### Почта
1. `yacli.mail.folders`
2. `yacli.mail.list` или `yacli.mail.search`
3. `yacli.mail.read`
4. Затем, если действительно нужно:
   - `yacli.mail.reply`
   - `yacli.mail.forward`
   - `yacli.mail.send`

### Вложения и инвайты
- `yacli.mail.attachment.export` для сохранения вложения на MCP host
- `yacli.mail.invite.inspect` для разбора calendar invite до действия
- `yacli.mail.invite.create_event` только после явного подтверждения пользователя

### Диск
1. `yacli.disk.info` или `yacli.disk.list`
2. `yacli.disk.mkdir`, если нужен целевой каталог
3. Затем один из вариантов:
   - `yacli.disk.upload` для приватной загрузки
   - `yacli.disk.upload_link` для загрузки с немедленной публичной ссылкой
   - `yacli.disk.publish` или `yacli.disk.unpublish` для уже существующих файлов
   - `yacli.disk.download` для выгрузки приватного файла на MCP host
4. Используйте `yacli.mail.send_link` или `yacli.mail.send_published_link`, если пользователь хочет отправить ссылку на файл по почте

### Календарь
1. `yacli.calendar.calendars`
2. `yacli.calendar.events`
3. Затем, если действительно нужно:
   - `yacli.calendar.create`
   - `yacli.calendar.delete`
- Для операций записи используйте явный calendar id
- Не предполагайте default calendar, если можно сначала получить список

### Правила безопасности
- Не отправляйте письма без явного подтверждения получателей и содержимого, если пользователь прямо не попросил отправить сейчас
- Не публикуйте приватные файлы и не создавайте публичные ссылки без явного подтверждения
- Не создавайте и не удаляйте события календаря без явного подтверждения
- Для destructive или externally visible действий сначала делайте read/list шаг, потом кратко описывайте план, потом выполняйте
