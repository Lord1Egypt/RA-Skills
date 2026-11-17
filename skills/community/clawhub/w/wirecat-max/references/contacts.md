# Контакты, заметки, псевдонимы, метки и упоминания

## Найти человека

`max personal contacts show` — человек по id, `@username` или части имени; имя, подходящее к нескольким, — ошибка
с кандидатами `[{ id, name, username }]`: взять id оттуда, не угадывать. `contacts block`, `unblock`, `rename` и
`account update --photo` меняют аккаунт владельца — только по его просьбе.

**Номер телефона не ставить в строку команды.** `max personal contacts lookup` читает его из трубы:
`printf '%s' "$номер" | max personal contacts lookup --json`.

Чтобы пересказать, что писал человек, вызывайте `contacts context <человек> --chat <чат> --limit <n>`
(в MCP — `chats` и `limit`); ответ — `{ at, text }` на сообщение. `-v` (в MCP `detail: 1`) — только
если нужны номера сообщений или локаторы. Связанные через `contacts link` аккаунты собирает только
`contacts context` без `--chat`; `contacts show` и `--chat` читают лишь названный аккаунт.
`contacts show` печатает номер телефона целиком; `--hide-phone` убирает его, когда ответ пойдёт дальше.
`contacts check` для MAX ничего не отправляет в списки спамеров; оценка — подсказка, не вывод.

## Личные заметки и псевдонимы

Псевдонимы хранятся локально для выбранного аккаунта; заметка о человеке видна в каждом профиле,
где он виден. Обновление контактов их не
затирает. `contacts rename` меняет запись в адресной книге мессенджера; `contacts aliases` —
только локальное имя. Если псевдоним неоднозначен, укажите id. Личные заметки отделены от
публичного описания человека. Показывайте и ищите их, когда это нужно для запроса владельца.

```sh
max personal contacts aliases set 101 'Project lead'
max personal contacts aliases remove 101
max personal contacts notes add 101 --file /path/to/own-note.md
max personal contacts notes list 101 --json
max personal contacts notes show 101 NOTE_ID --json
max personal contacts notes edit 101 NOTE_ID --revision 1 --file /path/to/own-note.md
max personal contacts notes remove 101 NOTE_ID
max personal contacts show 101 --with-notes --json
max personal contacts list 'notes:"follow up"' --json
max personal metadata show --chat CHAT_ID --json
max personal metadata sync --chat CHAT_ID --limit 1 --json
max personal tags rebuild --chat CHAT_ID --dry-run --json
max personal tags rebuild --chat CHAT_ID --sync-first --limit 1 --json
max personal tags list sources:auto --json
max personal tags remove news --chat CHAT_ID --source auto
```

## Метки каналов

Автоматические метки определяются по ключевым словам в сохранённых названиях, адресах и
описаниях групп и каналов. Модель и тексты сообщений не используются. Обновление описания
запрашивается явно; удалённый чат не меняется. `--dry-run` читает только сохранённые данные
и не сочетается с `--sync-first`. За запуск обрабатывается не более 500 чатов.
Оценка правила не является вероятностью. Ручные метки сохраняются при повторной классификации.
Без `--source` удаление метки убирает оба источника; следующий явный запуск `tags rebuild` может
создать автоматическую метку снова. Связывание людей не объединяет их личные заметки.

## Упоминания

Телефоны, почта, ссылки и документы Google из сохранённых сообщений хранятся как упоминания: их находят
правила при каждой записи в базу. `mentions list` принимает запрос: `kind:phone|email|url|document`,
`status:found|linked|dismissed`, `domain:` (сайт ссылки или адреса; `docs.google.com` значит `google.com`)
и `value:`; слово без поля — значение в любой записи, `89001234567` найдёт `+79001234567`. Сообщения,
сохранённые до появления упоминаний, читает один `mentions rebuild`. У каждой строки есть `locator`
сообщения; текст упоминаний — только владельцу, не в логи и не в файлы. Поиск сообщений понимает `phone:`, `email:`,
`url:` и `domain:` (почта в кавычках: `email:"ana@example.com"`). `mentions confirm <id> [person:<uid>|organization:<id>]`
записывает, чьё значение, `mentions reject <id>` отклоняет его насовсем; автор записи — агент или владелец
(`--as-owner`).

```sh
max personal mentions list kind:phone --json
max personal mentions list domain:google.com kind:url --json
max personal mentions show 12 --json
max personal mentions rebuild
max personal mentions confirm 12 person:<uid>
max personal mentions confirm 12 person:<uid> --all-in-chat   # имя: и все нерешённые места с ним в этом чате
max personal mentions list --new --json        # нерешённое с прошлого --new
max personal mentions domains --json           # сайты, на которые ведут ссылки, самые частые сверху
max personal mentions reject 12
```
