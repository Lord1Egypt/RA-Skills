# Step 9-10：更新作品 + 完成

## 前置读取

从任务目录读取以下文件，汇总所有变更：

1. **`meta.json`**：获取 `workId`
2. **`elements.json`**：获取完整元素列表，作为 ID 基准和原始数据参考
3. **`color-changes.json`**：获取配色变更的 `changes` 数组
4. **`text-changes.json`**：获取文本变更的 `changes` 数组
5. **`image-progress.json`**：获取 `status="uploaded"` 的图片条目及其 `cdnSrc`

## Step 9：构建更新负载并提交

## 执行门禁（必须遵守）

- 仅在前置步骤产物齐备且用户未终止任务时提交更新
- 本提交属于远端写操作，执行前应向用户展示变更摘要（配色/文本/图片数量）
- 本文命令为受控执行模板，实际执行前必须替换占位值并校验 payload

## 提交字段白名单（仅允许以下字段）

- `elements.{textElementId}.text`
- `elements.{textElementId}.fill`
- `elements.{rectElementId}.fill`
- `elements.{imageElementId}.image.src`
- `elements.{slideshowElementId}.assets[].id`
- `elements.{slideshowElementId}.assets[].src`

除上述白名单外，不构造或发送其他元素属性，避免非预期改动。

从三个变更文件合并构建最终更新负载：

### 合并规则

- **text 元素**：从 `color-changes.json` 取 `newFill`，从 `text-changes.json` 取 `newText`，合并为 `{ "text": "新文本", "fill": "#新颜色" }`
- **rect 元素**：从 `color-changes.json` 取 `newFill`，构建为 `{ "fill": "#新颜色" }`
- **image 元素**：从 `image-progress.json` 中 `source="image"` 且 `status="uploaded"` 的条目取 `cdnSrc`，构建为 `{ "image": { "src": "CDN链接" } }`
- **slideshow 元素**：从 `image-progress.json` 中 `source="slideshow"` 且 `status="uploaded"` 的条目，按 `slideshowElementId` 分组，构建 `assets` 数组：`{ "assets": [{ "id": "assetId", "src": "CDN链接" }] }`
- 失败或跳过的图片保留原始 `image.src` 不变（不包含在更新负载中）

### 提交更新

```bash
# 受控执行模板：仅提交白名单字段
curl -s -X POST \
  -H "Authorization: Bearer $WEIPAIBAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "elements": {
      "文本元素ID": { "text": "新的文本内容", "fill": "#333333" },
      "矩形元素ID": { "fill": "#1a5c2e" },
      "图片元素ID": { "image": { "src": "https://svg-cdn.creatby.com/..." } },
      "轮播元素ID": { "assets": [{ "id": "assetId1", "src": "https://svg-cdn.creatby.com/..." }, { "id": "assetId2", "src": "https://svg-cdn.creatby.com/..." }] }
    }
  }' \
  "${WEIPAIBAN_API_BASE:-https://weipaiban.cn}/api/v1/vectors/作品ID/parser"
```

### 更新规则

- `elements` 是一个对象，键为元素 ID，值为需要更新的属性
- text 元素：可同时更新 `text`（文本内容）和 `fill`（文字颜色）
- rect 元素：仅允许更新 `fill`（背景颜色）
- image 元素：仅允许更新 `image.src`（图片地址，使用 CDN 永久链接）
- slideshow 元素：通过 `assets` 数组更新轮播图片，每项需包含 `id`（asset ID，与 elements.json 中的 asset id 对应）和 `src`（新的 CDN 图片地址）。仅需包含需要更新的 asset，未包含的 asset 保持原图不变
- 元素的其他属性（布局、样式等）会保持不变
- 元素 ID 必须与 elements.json 中的 ID 对应

响应格式详见 [references/api-formats.md](../references/api-formats.md#parser-更新响应)。

## Step 10：完成

作品更新成功后，向用户展示：

1. 作品标题
2. 作品编辑链接：`${WEIPAIBAN_API_BASE:-https://weipaiban.cn}/vectors/作品ID`
3. 更新概要：替换了多少个配色元素、文本元素、图片元素和轮播图片
4. 提示用户可以在微排版编辑器中进一步调整

## 后置写入

将构建的完整更新负载写入任务目录的 `update-payload.json`（用于调试和审计）。更新 `meta.json` 的 `currentStep` 为 `"done"`。
