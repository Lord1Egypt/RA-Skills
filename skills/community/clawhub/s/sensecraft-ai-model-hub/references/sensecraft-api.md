# SenseCraft Public Model API

## One-line summary

SenseCraft public model download is a three-step flow:

1. `list_model` -> get model IDs
2. `view_model` -> get `data.file_url`
3. download from `file_url`

## Base URL

```text
https://sensecraft.seeed.cc/aiserverapi
```

## Authentication

Public model library access is expected to work anonymously.

Operational assumptions:
- send `appid=131` by default
- do not send `Authorization` unless required by future evidence
- handle per-model failures gracefully during bulk runs

## Endpoint: list_model

```http
GET /model/list_model
```

### Common parameters
- `appid=131`
- `length`
- `page`
- `search`
- `uniform_type`
- repeated `task`

### Important response fields
- `data.count`
- `data.list[]`
- `data.list[].id`
- `data.list[].name`
- `data.list[].description`
- `data.list[].uniform_types`
- `data.list[].task`

### Important caveat

This endpoint does **not** directly return the final downloadable model URL.

## Endpoint: view_model

```http
GET /model/view_model
```

### Parameters
- `appid=131`
- `model_id=<ID>`

### Important response fields
- `data.id`
- `data.name`
- `data.description`
- `data.file_url`
- `data.model_format`
- `data.uniform_types`
- `data.task`

### Critical field

`data.file_url` is the actual model download URL.

## Download behavior

Follow redirects while downloading.

Shell shape:

```bash
curl -L 'FILE_URL' -o output.bin
```

The bundled script improves on this by:
- retrying transient failures
- inferring a file extension from the final response when possible
- emitting a manifest after download

## Bulk crawling strategy

1. request page 1 from `list_model`
2. read `data.count`
3. compute total pages from `count` and `length`
4. collect every model ID from every page
5. call `view_model` for each ID
6. export detail records to JSON or CSV
7. optionally export an aggregate summary
8. optionally download selected artifacts

## Suggested fields for exported indexes

- `id`
- `name`
- `description`
- `task`
- `uniform_types`
- `model_format`
- `file_url`
- filename / extension hints
- whether the URL looks TFLite-like
- raw detail payload when useful

## Failure handling

During bulk jobs:
- skip individual detail failures
- record warnings
- keep the crawl going
- use mild throttling rather than unrestricted concurrency
- retry transient failures a small number of times
