# 使用说明

## 适用范围

`qiniu_object_storage` 只负责：

- 上传本地文件到七牛
- 根据空间可见性返回交付链接
- 为私有空间生成带时效的签名下载链接

它不负责任何图片或视频生成。

## 默认返回规则

- 当 `api_key/qiniu.json` 中存在 `"is_private": true`，或环境变量 `QINIU_IS_PRIVATE=true` 时，默认返回签名链接
- 当空间是公开的，默认返回公网链接
- 如需覆盖默认行为，可显式传 `--private-url` 或 `--public-url`

## 运行方式

```powershell
uv run --python python scripts/upload_file.py --file <本地文件>
uv run --python python scripts/upload_file.py --file <本地文件> --private-url --expires-in 600
uv run --python python scripts/upload_file.py --file <本地文件> --public-url
uv run --python python scripts/generate_private_download_url.py --key <对象key> --expires-in 600
```

## 对象 key 规则

- 若文件位于 `outputs/` 目录内，优先复用相对路径作为对象 key
- 若文件位于其他目录，可通过 `--key` 明确指定，或通过 `--prefix` 自动生成

## 输出字段

- `storage_provider=qiniu`
- `bucket`
- `object_key`
- `access_mode`
- `delivery_url`
- 可选 `public_url`
- 可选 `private_url`
- 可选 `base_url`
- 私有链接场景可带 `expires_in`

## 与其他 skill 的关系

- 它通常被图片/视频 workflow 或 `media-gen` Agent 在交付阶段调用
- 它不应决定内容生成供应商
