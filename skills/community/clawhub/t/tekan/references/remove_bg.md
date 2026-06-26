# Remove Background 模块

去除产品图片的背景。通常是商品模特图工作流的第一步 — 输出的 `bgRemovedImageFileId` 直接传给 `product_avatar.py --product-image-no-bg`。

## 使用场景

- 当你需要一张透明/去背的产品图片，然后放入模特场景。
- 作为 Product Avatar V3 流程的第 1 步：**去除背景 → 替换产品图片**。

## 子命令

| 子命令 | 使用场景 | 轮询？ |
|------------|-------------|--------|
| `run` | **默认。** 新请求，从提交到完成 | 是 — 等待至完成 |
| `submit` | 批量：提交多个任务不等待 | 否 — 立即退出 |
| `query` | 恢复：对已有的 `taskId` 继续轮询 | 是 — 等待至完成 |

## 用法

```bash
python {baseDir}/scripts/remove_bg.py <subcommand> [options]
```

## 示例

### `run` — 完整流程（默认）

```bash
python {baseDir}/scripts/remove_bg.py run --image product.png
```

下载结果图片：

```bash
python {baseDir}/scripts/remove_bg.py run --image product.png --output product_nobg.png
```

### 商品模特图工作流（两步）

```bash
# 第 1 步：去除背景 — 记录输出中的 bgRemovedImageFileId
python {baseDir}/scripts/remove_bg.py run --image product.png --json

# 第 2 步：将 fileId 传给 product_avatar
python {baseDir}/scripts/product_avatar.py run \
  --product-image-no-bg <bgRemovedImageFileId> \
  --avatar-id <avatarId>
```

### `query` — 恢复

```bash
python {baseDir}/scripts/remove_bg.py query --task-id <taskId> --timeout 600
```

## 选项

### `run` 和 `submit`

| 选项 | 说明 |
|--------|-------------|
| `--image` | 产品图片 fileId 或本地路径（必需） |
| `--notice-url URL` | 完成通知的 Webhook URL |

### 轮询（`run` 和 `query`）

| 选项 | 说明 |
|--------|-------------|
| `--timeout SECS` | 最大轮询时间，单位秒（默认：300） |
| `--interval SECS` | 轮询间隔，单位秒（默认：3） |

### 全局

| 选项 | 说明 |
|--------|-------------|
| `--output FILE` | 将结果图片下载到本地路径 |
| `--json` | 输出完整 JSON 响应 |
| `-q, --quiet` | 静默模式，抑制 stderr 状态消息 |

## 输出字段

| 字段 | 说明 |
|-------|-------------|
| `bgRemovedImageFileId` | 去背图片的 FileId — 传给 `product_avatar.py --product-image-no-bg` |
| `bgRemovedImagePath` | 去背图片的 URL |
| `bgRemovedImageWidth/Height` | 结果图片尺寸 |
| `maskImageFileId` | 蒙版图片的 FileId |
| `maskImagePath` | 蒙版图片的 URL |
| `costCredit` | 消耗的积分 |

## 任务状态

`init` → `running` → `success` 或 `fail`
