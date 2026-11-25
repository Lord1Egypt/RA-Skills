<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Yandex Disk API: disk/resources

## `ydisk api resources-copy [options]`

- What: Создать копию файла или папки
- Call: `POST /v1/disk/resources/copy`, effect: write
- Permission keys: `files.delete`, `files.copy`

| Flag | Required | What |
|---|---|---|
| `--from <value>` | yes | Путь к копируемому ресурсу. |
| `--path <value>` | yes | Путь к создаваемому ресурсу. |
| `--fields <value>` | no | Список возвращаемых атрибутов. |
| `--force-async <value>` | no | Выполнить асинхронно. |
| `--overwrite <value>` | no | Перезаписать существующий ресурс. |

## `ydisk api resources-create [options]`

- What: Создать каталог
- Call: `PUT /v1/disk/resources`, effect: write
- Permission keys: `files.create`

| Flag | Required | What |
|---|---|---|
| `--path <value>` | yes | Путь к создаваемой папке. |
| `--fields <value>` | no | Список возвращаемых атрибутов. |

## `ydisk api resources-delete [options]`

- What: Удалить файл или папку
- Call: `DELETE /v1/disk/resources`, effect: destructive
- Permission keys: `files.delete`

| Flag | Required | What |
|---|---|---|
| `--path <value>` | yes | Путь к файлу или папке. |
| `--fields <value>` | no | Список возвращаемых атрибутов. |
| `--force-async <value>` | no | Выполнить асинхронно. |
| `--md5 <value>` | no | md5 удаляемого файла. |
| `--permanently <value>` | no | Удалить ресурс не помещая в Корзину. |

## `ydisk api resources-files-list [options]`

- What: Получить список файлов упорядоченный по имени
- Call: `GET /v1/disk/resources/files`, effect: read
- Pages: offset: send `offset` (query), raised by the items read so far; items in `items`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--fields <value>` | no | Список возвращаемых атрибутов. |
| `--limit <value>` | no | Количество последних загруженных файлов в ответе. |
| `--media-type <value>` | no | Фильтр по медиа типу. Несколько типов перечисляются через запятую. |
| `--offset <value>` | no | Смещение от начала списка вложенных ресурсов. |
| `--preview-crop <value>` | no | Разрешить обрезку превью. |
| `--preview-size <value>` | no | Размер превью. |
| `--sort <value>` | no | Поле для сортировки ресурсов. |
| `--all` | no | read every page, as the API pages it |

## `ydisk api resources-last-uploaded-list [options]`

- What: Получить список файлов упорядоченный по дате загрузки
- Call: `GET /v1/disk/resources/last-uploaded`, effect: read

| Flag | Required | What |
|---|---|---|
| `--fields <value>` | no | Список возвращаемых атрибутов. |
| `--limit <value>` | no | Количество последних загруженных файлов в ответе. |
| `--media-type <value>` | no | Фильтр по медиа типу. Несколько типов перечисляются через запятую. |
| `--preview-crop <value>` | no | Разрешить обрезку превью. |
| `--preview-size <value>` | no | Размер превью. |

## `ydisk api resources-list [options]`

- What: Получить метаинформацию о файле или каталоге
- Call: `GET /v1/disk/resources`, effect: read
- Pages: offset: send `offset` (query), raised by the items read so far; items in `_embedded.items`; the count of all in `_embedded.total`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--path <value>` | yes | Путь к ресурсу. |
| `--fields <value>` | no | Список возвращаемых атрибутов. |
| `--limit <value>` | no | Количество выводимых вложенных ресурсов. |
| `--offset <value>` | no | Смещение от начала списка вложенных ресурсов. |
| `--preview-crop <value>` | no | Разрешить обрезку превью. |
| `--preview-size <value>` | no | Размер превью. |
| `--sort <value>` | no | Поле для сортировки вложенных ресурсов. |
| `--all` | no | read every page, as the API pages it |

## `ydisk api resources-move [options]`

- What: Переместить файл или папку
- Call: `POST /v1/disk/resources/move`, effect: write
- Permission keys: `files.delete`, `files.move`

| Flag | Required | What |
|---|---|---|
| `--from <value>` | yes | Путь к перемещаемому ресурсу. |
| `--path <value>` | yes | Путь к создаваемому ресурсу. |
| `--fields <value>` | no | Список возвращаемых атрибутов. |
| `--force-async <value>` | no | Выполнить асинхронно. |
| `--overwrite <value>` | no | Перезаписать существующий ресурс. |

## `ydisk api resources-public-list [options]`

- What: Получить список опубликованных ресурсов
- Call: `GET /v1/disk/resources/public`, effect: read
- Pages: offset: send `offset` (query), raised by the items read so far; items in `items`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--fields <value>` | no | Список возвращаемых атрибутов. |
| `--limit <value>` | no | Количество выводимых ресурсов. |
| `--offset <value>` | no | Смещение от начала списка ресурсов. |
| `--preview-crop <value>` | no | Разрешить обрезку превью. |
| `--preview-size <value>` | no | Размер превью. |
| `--type <value>` | no | Фильтр по типам ресурсов. |
| `--all` | no | read every page, as the API pages it |

## `ydisk api resources-publish [options]`

- What: Опубликовать ресурс
- Call: `PUT /v1/disk/resources/publish`, effect: write
- Permission keys: `files.share`, `files.publish`
- Body: `PublishResource`, required

| Flag | Required | What |
|---|---|---|
| `--path <value>` | yes | Путь к публикуемому ресурсу. |
| `--allow-address-access <value>` | no | Возможность клиента обрабатывать ответы от адресного доступа. |
| `--fields <value>` | no | Список возвращаемых атрибутов. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `ydisk api resources-unpublish [options]`

- What: Отменить публикацию ресурса
- Call: `PUT /v1/disk/resources/unpublish`, effect: write
- Permission keys: `files.share`, `files.unpublish`

| Flag | Required | What |
|---|---|---|
| `--path <value>` | yes | Путь к ресурсу. |
| `--fields <value>` | no | Список возвращаемых атрибутов. |

## `ydisk api resources-update [options]`

- What: Обновить пользовательские данные ресурса
- Call: `PATCH /v1/disk/resources`, effect: write
- Body: `ResourcePatch`, required

| Flag | Required | What |
|---|---|---|
| `--path <value>` | yes | Путь к обновляемому ресурсу. |
| `--fields <value>` | no | Список возвращаемых атрибутов. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `ydisk api resources-upload-url [options]`

- What: Загрузить файл в Диск по URL
- Call: `POST /v1/disk/resources/upload`, effect: write
- Permission keys: `files.upload`

| Flag | Required | What |
|---|---|---|
| `--path <value>` | yes | Путь, куда будет помещён ресурс. |
| `--url <value>` | yes | URL внешнего ресурса, который следует загрузить. |
| `--disable-redirects <value>` | no | Запретить делать редиректы. |
| `--fields <value>` | no | Список возвращаемых атрибутов. |
