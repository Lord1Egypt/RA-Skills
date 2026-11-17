# Статистика, рейтинги и графики

Отчёты читают только сохранённые данные; неполный архив даёт нижнюю границу, а неизвестное не равно нулю.

## Имена в статистических запросах

Владелец может назвать чат или человека обычным именем. Находите чат через `chats list`,
человека через `contacts show` / `contacts list` или сохранённых авторов через `stats contacts top`;
для отчёта используйте подтверждённый ID нужного аккаунта. Если совпадений несколько,
покажите кандидатов и уточните выбор. Не угадывайте ID и не превращайте неизвестное имя
в утверждение о нулевой активности. При неудачном поиске объясните, какое имя, @username
или уточнение аккаунта поможет. Счётчики относятся только к наблюдаемой истории.

Статистический `--answerer` также принимает сохранённое имя, своё имя и @username напрямую,
без подключения. При неоднозначности используйте возвращённые кандидаты нужного аккаунта,
не угадывайте. `identity_known: false` вместе с `status: unknown` означает, что явно выбранный
ID не наблюдался; ноль ответов не доказывает нулевую активность.

## Подсчёт

Для количества совпадений в архиве используй `max personal stats messages show [запрос] --by chat|sender|day|hour --json`:
одна запись считается один раз. Проверяй `missing`: неполный архив даёт нижнюю границу. Отчёт — один `{item}`,
`--jsonl` он не принимает. `--source max` явно включает другие сохранённые профили; обычный вызов остаётся в текущей
учётной записи.

## Активность чата

MCP `max_read` с `command: "stats chats show"` читает активность из архива без запроса вступлений и выходов.
`members` отсутствует; число сообщений неполного архива — нижняя граница, медианы и доли могут отличаться.
В CLI: `max personal stats chats show <чат> --offline --json`.

## Рейтинги

Рейтинги архива: `max personal stats messages top` / `max personal stats contacts top` — метрика `--measure` или
`--score helpful|active|engaging`; оценки используют всю допустимую выборку до limit.
Читай coverage/quality и исключения: неизвестные счётчики не равны нулю, свежесть наблюдений показана по полям;
старые значения остаются unknown. Используй `selection` строки и шаг `stats.evidence` из `next` для
`stats messages evidence` / `stats contacts evidence`,
продолжай по `cursor` шага `page.next`; при изменении данных начни без cursor.
Руководство: [рейтинги](https://github.com/WireCatLabs/max-cli/blob/main/docs/rankings.md).

Для вопросов без наблюдаемого ответа используй `stats messages unanswered`; время ответа явно
выбранных людей — `stats contacts responses --answerer <person>`. Помощь новичкам с известной датой
вступления — `stats chats newcomers <chat>`, посты каналов с просмотрами и малым обсуждением —
`stats messages discussion`. Проверяй качество архива и reply-графа, копируй точную `selection` строки
с `--component report`. Неизвестные история и дата вступления не равны нулю. Отчёты читают только
сохранённые данные; не выводи из выбранных id, кто был админом в прошлом.

## Удержание

Удержание: `max personal stats chats retention <chat> --checkpoints 1d,7d,30d --within 7d --json`.
Используй только известные joined_at; partial absence и пропущенные снимки — unknown, будущие окна — pending.
Показывай observable знаменатель, неизвестные и фактическую дату снимка; не называй это непрерывным участием.
Сообщения когорты — через `stats messages evidence --component report` с точной `selection` строки.

## Счётчики просмотров и реакций

Счётчики: `max personal stats messages counters show --chat <chat> --counters views,reactions --json`.
Проверяй observed_at/source/freshness каждого поля (24h по умолчанию). Refresh — remote read + local write:
`stats messages counters sync --chat <chat> --max-messages 20 --sync-time 30s --dry-run --json`.
Предпросмотр не подключается. Реальный refresh требует разрешённой записи и явного chat или pinned selection;
никогда не освежай весь аккаунт неявно. MAX поддерживает views/reactions; comments unsupported.
Не отправляй, не отмечай прочтение и не вызывай increment views. Сохранённые значения без наблюдения — unknown.

## Графики

`max personal stats charts <chat> --json` возвращает нейтральный JSON; `--output activity.svg` или
`--output activity.png` также пишет новое изображение с тёмной темой. `--chart-kind messages|active|membership`,
`--by day|week`, `--since-time`, `--timezone` задают вид и период. Пропуски — null, partial означает неполные данные.
Membership недоступен offline; MCP `max_read` (`command: "stats charts"`) отдаёт JSON без файлов и подключения;
`format: "png"` добавляет PNG image content и JSON с данными и размером.
