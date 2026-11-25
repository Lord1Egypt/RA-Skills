<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Yandex Disk API: disk/public/resources

## `ydisk api public-resources-get [options]`

- What: Получить метаинформацию о публичном файле или каталоге
- Call: `GET /v1/disk/public/resources`, effect: read
- Pages: offset: send `offset` (query), raised by the items read so far; items in `_embedded.items`; the count of all in `_embedded.total`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--public-key <value>` | yes | Ключ или публичный URL ресурса. |
| `--fields <value>` | no | Список возвращаемых атрибутов. |
| `--limit <value>` | no | Количество выводимых вложенных ресурсов. |
| `--offset <value>` | no | Смещение от начала списка вложенных ресурсов. |
| `--path <value>` | no | Путь к ресурсу в публичной папке. |
| `--preview-crop <value>` | no | Разрешить обрезку превью. |
| `--preview-size <value>` | no | Размер превью. |
| `--sort <value>` | no | Поле для сортировки вложенных ресурсов. |
| `--all` | no | read every page, as the API pages it |

## `ydisk api public-resources-save-to-disk [options]`

- What: Сохранить публичный ресурс в папку Загрузки
- Call: `POST /v1/disk/public/resources/save-to-disk`, effect: write
- Permission keys: `files.upload`

| Flag | Required | What |
|---|---|---|
| `--public-key <value>` | yes | Ключ или публичный URL ресурса. |
| `--fields <value>` | no | Список возвращаемых атрибутов. |
| `--force-async <value>` | no | Выполнить асинхронно. |
| `--name <value>` | no | Имя, под которым ресурс будет сохранён в папке. |
| `--path <value>` | no | Путь к копируемому ресурсу в публичной папке. |
| `--save-path <value>` | no | Путь к папке, в которую будет сохранен ресурс. По умолчанию «Загрузки». |

## `ydisk api public-settings-update [options]`

- What: Обновить настройки публичных ссылок
- Call: `PATCH /v1/disk/public/resources/public-settings`, effect: write
- Permission keys: `files.share`
- Body: `UpdatePublicSettings`, required

| Flag | Required | What |
|---|---|---|
| `--path <value>` | yes | Путь к ресурсу. |
| `--fields <value>` | no | Список возвращаемых атрибутов. |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
