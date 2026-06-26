# Product Avatar 模块

在数字人（模特）场景中替换商品图片 — 自动将你的产品放到模特手中。

## 使用场景

当你需要将产品放入数字人/模特场景中 — 例如让模特手持、佩戴或展示你的产品。

## 子命令

| 子命令 | 使用场景 | 轮询？ |
|------------|-------------|--------|
| `run` | **默认。** 新请求，从提交到完成 | 是 — 等待至完成 |
| `submit` | 批量：提交多个任务不等待 | 否 — 立即退出 |
| `query` | 恢复：对已有的 `taskId` 继续轮询 | 是 — 等待至完成 |
| `list-categories` | 列出模特分类（用于筛选 `list-avatars`） | 否 |
| `list-avatars` | 浏览公共模特模板 | 否 |

## 用法

```bash
python {baseDir}/scripts/product_avatar.py <subcommand> [options]
```

## 完整工作流（去除背景 → 替换）

推荐的 Product Avatar V3 流程：

```
第 1 步：productImage → remove_bg.py → bgRemovedImageFileId
第 2 步：bgRemovedImageFileId + avatarId → product_avatar.py → resultImage
```

```bash
# 第 1 步 — 去除产品背景
python {baseDir}/scripts/remove_bg.py run --image product.png --json
# 记录输出中的 bgRemovedImageFileId

# 第 2 步 — 浏览可用模特并选择一个
python {baseDir}/scripts/product_avatar.py list-avatars --gender female

# 第 3 步 — 将产品替换到模特场景中
python {baseDir}/scripts/product_avatar.py run \
  --product-image-no-bg <bgRemovedImageFileId> \
  --avatar-id <avatarId>
```

如果你已经有去除背景的产品图片或自定义模板图片，可以跳过第 1 步直接进入第 2/3 步。

## 浏览模板

### 列出分类

```bash
python {baseDir}/scripts/product_avatar.py list-categories
```

### 浏览模特

```bash
# 所有模特
python {baseDir}/scripts/product_avatar.py list-avatars

# 按性别筛选
python {baseDir}/scripts/product_avatar.py list-avatars --gender female

# 按分类筛选
python {baseDir}/scripts/product_avatar.py list-avatars --category-ids <id1>,<id2>

# 按最新排序
python {baseDir}/scripts/product_avatar.py list-avatars --sort Newest
```

### `list-avatars` 选项

| 选项 | 说明 |
|--------|-------------|
| `--gender` | `male` 或 `female` |
| `--category-ids` | 分类 ID，逗号分隔（来自 `list-categories`） |
| `--ethnicity-ids` | 族裔 ID，逗号分隔 |
| `--sort` | `Popularity`（默认）或 `Newest` |
| `--page` | 页码（默认：1） |
| `--size` | 每页条数（默认：20） |

## 示例

### 自动模式（模特优先）

```bash
python {baseDir}/scripts/product_avatar.py run \
  --product-image product.png \
  --template-image template.png \
  --mode auto \
  --keep-target model
```

### 自动模式（产品优先）

```bash
python {baseDir}/scripts/product_avatar.py run \
  --product-image product.png \
  --template-image template.png \
  --mode auto \
  --keep-target product
```

### 手动模式 V4 (banana_pro)

```bash
python {baseDir}/scripts/product_avatar.py run \
  --product-image product.png \
  --template-image template.png \
  --mode manual \
  --version v4 \
  --location '[[10.5, 20.0], [30.5, 40.0]]'
```

### 使用已去背的产品图（来自 remove_bg.py）

```bash
python {baseDir}/scripts/product_avatar.py run \
  --product-image-no-bg <bgRemovedImageFileId> \
  --avatar-id <avatarId>
```

### 使用公共模特（来自 list-avatars）

```bash
python {baseDir}/scripts/product_avatar.py run \
  --product-image product.png \
  --avatar-id <avatarId>
```

## 选项

### `run` 和 `submit`

| 选项 | 说明 |
|--------|-------------|
| `--product-image` | 产品图片 fileId 或本地路径 |
| `--product-image-no-bg` | 已去背的产品图片 fileId 或本地路径 |
| `--template-image` | 模板/模特图片 fileId 或本地路径 |
| `--avatar-id` | 模特 ID（公共或私有数字人） |
| `--face-image` | 用户面部图片 fileId 或本地路径 |
| `--prompt` | 图片编辑提示词 |
| `--mode` | `auto`（自动）或 `manual`（基于坐标） |
| `--keep-target` | `model`（默认）或 `product`；仅用于自动模式 |
| `--version` | `v3`（默认）或 `v4`（banana_pro，支持手动模式） |
| `--location` | 产品坐标，JSON 二维数组 |
| `--product-size` | 产品尺寸（枚举值） |
| `--project-id` | 项目 ID |
| `--board-id` | 看板 ID |
| `--notice-url` | Webhook URL |

### 轮询 / 全局

| 选项 | 说明 |
|--------|-------------|
| `--timeout SECS` | 最大轮询时间（默认：600） |
| `--interval SECS` | 轮询间隔（默认：5） |
| `--output FILE` | 将结果下载到本地路径 |
| `--json` | 输出完整 JSON 响应 |
| `-q, --quiet` | 静默模式，抑制状态消息 |

## 模式对比

| 模式 | 版本 | 说明 |
|------|---------|-------------|
| `auto` + `model` | v3/v4 | 自动放置，保留模特姿势（默认） |
| `auto` + `product` | v3/v4 | 自动放置，保留产品外观 |
| `manual` | 仅 v4 | 基于坐标的手动放置（banana_pro） |

## 费用

固定：每任务 **0.5 积分**。失败的任务会退还积分。
