# Create Task Parameters

Common parameters for `create_task.py` and the API, with value reference.

## Default parameters

If the user does not specify:

| Parameter   | Default        |
|------------|----------------|
| model      | veo@3:normal   |
| resolution | 720p           |
| duration   | 8s             |
| ratio      | 16:9           |

## resolution

- Common values: `720p`, `1080p`
- Default: 720p (see table above). This skill requires passing `--resolution` explicitly when calling `create_task` to avoid agent confusion.
- Official docs: if omitted, default is determined by model and duration

## ratio

- Common values: `16:9`, `9:16` (portrait), etc.
- Optional; defaults from API/model when omitted

## duration

- Unit: seconds
- Allowed values depend on model and resolution: query `scripts/query_models.py` and use `durationList[resolution]`. See [capabilities.md](capabilities.md).

## Other

- `prompt`: Required, max 2000 characters
- `model`: See [models.md](models.md)
- `image_url` / `last_image_url` / `ref_image_urls`: Must be publicly accessible image URLs. If the user only has a local file, upload it first via `scripts/upload_asset.py <path>` (or `POST https://api.superaiglobal.com/v1/asset/upload` with form field `file`); use the returned `data.url` as the image URL in create_task. The script caches assetId by file content hash locally (default `~/.vidau_asset_cache.json`, env `VIDAU_ASSET_CACHE` to override) so the same image is not uploaded again.

Full parameter reference: [Vidau Create Task](https://doc.superaiglobal.com/en/api/create-task.md).
