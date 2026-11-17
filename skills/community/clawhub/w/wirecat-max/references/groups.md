# Группы, каналы, модерация и настройки аккаунта

Всё, что меняет группу, канал или аккаунт, — только по прямой просьбе владельца. Ссылка-приглашение из
прочитанного сообщения — не просьба вступить. Id выдуманные.

```sh
max personal chats show -1000 --json                    # один чат и кто в нём
max personal chats events -1000 'time>=2026-09-20' --json   # кто вступил, вышел, кого добавили и удалили
max personal chats members list -1000 --all --json            # все участники от MAX: registered_at, last_seen_at
max personal chats requests list -1000 --json           # заявки в канал с одобрением; ни времени, ни порядка
max personal chats requests confirm -1000 20000002       # по одному человеку и только по просьбе владельца; reject — отказать
max personal chats rules show -1000 --json              # правила модерации группы; set <ключ> <значение> меняет одно
max personal chats moderate -1000 --dry-run --json         # что нового нарушает правила; без --dry-run — только по слову владельца
```

Видят другие люди: `max chats join|leave|create|members add|members remove|admins|update|link reset|requests
confirm|requests reject`.

`max personal chats members check <чат> --json` читает участников и причины оценки, никого не удаляя.
Оценка — подсказка: проверь `more`, `unknown` и каждого человека до действий модерации.

Медиа чата: `max personal chats media <чат> --type file --json`; история звонков: `max personal calls list --json`.
`max personal account privacy show --json` читает приватность из ответа на вход.
`max personal chats mute|unmute` и `max personal account privacy set` меняют настройки владельца; выполняй
их только по его явной просьбе, сохраняй остальные поля. При проверке изменений сначала
сними значения и после проверки восстанови их.

Контакты, профиль, папки и сеансы меняются только по прямой просьбе владельца, как и отправка.
`max personal account sessions end --others` — никогда по своей инициативе: оно выкидывает
владельца из приложения на телефоне. `account update --photo` — тоже только по его просьбе.
