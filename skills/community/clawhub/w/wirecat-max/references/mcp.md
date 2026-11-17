# MCP: инструменты, удалённый доступ и разговоры

## Инструменты

Сначала `max_tools_search`, затем `max_read` или `max_write` с `{command, arguments}`.
Команда совпадает с CLI-путём, например `stats messages show`; прежние per-command имена
не вызываются. Для бота — `max_bot_tools_search/read/write`, команда без `bot` ([бот](bot.md)). Форм нет: права
профиля решают доступ, `ask` в MCP разрешает вызванную запись; CLI подтверждения сохраняются.
Через MCP вход недоступен ([установка](setup.md#первый-запуск)).

MCP `inbox`/`review` принимают `kinds` и `new`; отметки новых сообщений отдельны от CLI.
MCP `max_read` с `command: "stats chats show"` — [статистика](stats.md#активность-чата).
Отложенная отправка через MCP — [отправка](sending.md#отложенная-отправка).

## Удалённый сервер

`max personal mcp serve --http --public-url https://<имя>.ts.net` работает через HTTPS-туннель со входом по коду.
Права `deny`/`readonly` запрещают запись; `ask`/`allow` допускают запрошенное действие без серверной формы.
`--permission ключ=уровень` временно ужесточает права, ослабить их не может. Агент не меняет права для обхода отказа.
`max personal mcp revoke` завершает входы приложений этого профиля.
Клиенту MCP без терминала (Claude Desktop) готовую запись с полными путями печатает `max personal mcp config`.

## Разговоры

В MCP `max_read` с `command` `"conversations list"`, `"conversations show"`, `"search conversations"`,
`"conversations related"` и `"conversations status"` читает построенное, а `max_write` (`command: "conversations rebuild"`)
догоняет на этом компьютере. Через MCP агент получает инструкцию `link-conversations`, оценивает объём инструментом
`max_read` (`command: "conversations batches status"`) и ждёт согласия владельца для этого чата. Затем читает
`max_read` (`command: "conversations batches show"`), сохраняет ответы через `max_write` (`command: "conversations links add"`) и перестраивает граф через
`max_write` (`command: "conversations links rebuild"`). `max_write` (`command: "conversations links clear"`) удаляет ответы агента; после него граф также нужно
перестроить. Запись требует `conversations.links`. Настройка внешних векторов действует и на MCP-поиск: вопрос
отправляется выбранному сервису.

## Файлы удалённому агенту

Байты сохранённого файла и страницы PDF — [вложения](attachments.md#удалённый-агент).
