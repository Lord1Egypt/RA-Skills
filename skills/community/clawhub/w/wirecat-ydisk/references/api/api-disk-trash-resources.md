<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Yandex Disk API: disk/trash/resources

## `ydisk api trash-resources-delete [options]`

- What: Очистить Корзину
- Call: `DELETE /v1/disk/trash/resources`, effect: destructive
- Permission keys: `files.delete`

| Flag | Required | What |
|---|---|---|
| `--apply-photoslice-filter <value>` | no | Требуется ли удалять только файлы фотосреза |
| `--fields <value>` | no | Список возвращаемых атрибутов. |
| `--force-async <value>` | no | Выполнить асинхронно. |
| `--path <value>` | no | Путь к ресурсу в Корзине. |

## `ydisk api trash-resources-list [options]`

- What: Получить содержимое Корзины
- Call: `GET /v1/disk/trash/resources`, effect: read
- Pages: offset: send `offset` (query), raised by the items read so far; items in `_embedded.items`; the count of all in `_embedded.total`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--path <value>` | yes | Путь к ресурсу в Корзине. |
| `--apply-photoslice-filter <value>` | no | Требуется ли отдавать только фотосрез |
| `--fields <value>` | no | Список возвращаемых атрибутов. |
| `--limit <value>` | no | Количество выводимых вложенных ресурсов. |
| `--offset <value>` | no | Смещение от начала списка вложенных ресурсов. |
| `--preview-crop <value>` | no | Разрешить обрезку превью. |
| `--preview-size <value>` | no | Размер превью. |
| `--sort <value>` | no | Поле для сортировки вложенных ресурсов. |
| `--all` | no | read every page, as the API pages it |

## `ydisk api trash-resources-restore [options]`

- What: Восстановить ресурс из Корзины
- Call: `PUT /v1/disk/trash/resources/restore`, effect: write
- Permission keys: `files.delete`, `files.restore`

| Flag | Required | What |
|---|---|---|
| `--path <value>` | yes | Путь к ресурсу в Корзине. |
| `--fields <value>` | no | Список возвращаемых атрибутов. |
| `--force-async <value>` | no | Выполнить асинхронно. |
| `--name <value>` | no | Имя, под которым будет восстановлен ресурс. |
| `--overwrite <value>` | no | Перезаписать существующий ресурс восстанавливаемым. |
