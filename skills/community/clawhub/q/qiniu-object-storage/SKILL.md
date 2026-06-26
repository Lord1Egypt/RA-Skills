---
name: qiniu_object_storage
description: 上传本地文件到七牛对象存储，返回可交付的下载链接。当用户提到"上传""七牛""对象存储""OSS""交付链接""公网链接""签名链接"时引用；当已有本地文件需要上传并获得可访问的 URL 时引用；当工作流完成内容生成后进入交付阶段时引用。自动按扩展名判定文件类型，私有空间返回签名链接，公开空间返回公网链接。
metadata:
  openclaw:
    requires:
      bins:
        - uv
      anyBins:
        - python
        - python3
        - py
      env:
        - QINIU_ACCESS_KEY
        - QINIU_SECRET_KEY
        - QINIU_BUCKET
        - QINIU_PUBLIC_DOMAIN
        - QINIU_IS_PRIVATE
    primaryEnv: QINIU_ACCESS_KEY
---

# 七牛对象存储

这个 skill 只负责文件上传与交付链接，不负责图片或视频生成。

适用场景：

- 已有本地文件，需要上传到七牛
- 需要返回一个可直接交付的下载链接
- 私有空间需要带时效签名链接

## 默认行为

- 对象 key 自动生成为 `日期/类型/文件名`，如 `20260327/images/photo.png`
- 类型按扩展名自动判定：images / videos / audio / others
- 如果配置里声明空间是私有的，上传后默认返回签名链接
- 如果配置里声明空间是公开的，上传后默认返回公网链接
- 只有用户明确要求，或脚本显式传 `--private-url` / `--public-url` 时，才覆盖默认行为

## 使用脚本

脚本位于 skill 目录内的 `scripts/`，运行时始终使用绝对路径。

设 `QINIU_SKILL_DIR` 为 `.claude/skills/qiniu_object_storage` 的绝对路径：

- 上传文件并按空间配置返回默认交付链接：`uv run --python python $QINIU_SKILL_DIR/scripts/upload_file.py --file <本地文件>`
- 强制返回私有签名链接：`uv run --python python $QINIU_SKILL_DIR/scripts/upload_file.py --file <本地文件> --private-url --expires-in 600`
- 强制返回公网链接：`uv run --python python $QINIU_SKILL_DIR/scripts/upload_file.py --file <本地文件> --public-url`
- 已有对象 key，生成私有签名链接：`uv run --python python $QINIU_SKILL_DIR/scripts/generate_private_download_url.py --key <对象key> --expires-in 600`

## 输出约定

- 输出 JSON 至少包含：
  - `storage_provider`
  - `bucket`
  - `object_key`
  - `access_mode`
  - `delivery_url`
- 可能额外包含：
  - `public_url`
  - `private_url`
  - `base_url`
  - `expires_in`

## 配置

仅通过环境变量配置，缺失时抛出异常：

| 环境变量 | 说明 |
|---|---|
| `QINIU_ACCESS_KEY` | 七牛 Access Key（主标识） |
| `QINIU_SECRET_KEY` | 七牛 Secret Key |
| `QINIU_BUCKET` | 存储空间名称 |
| `QINIU_PUBLIC_DOMAIN` | 公网访问域名 |
| `QINIU_IS_PRIVATE` | 是否为私有空间（可选，默认 false） |

## 协作方式

- 它通常是图片或视频 workflow 的交付步骤
- 当用户只要求上传已有文件时，也可以单独调用
- 它不应决定前置内容由哪个 AI 供应商生成
