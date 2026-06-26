# Step 8d：图片上传 CDN

将所有生成的图片逐张上传到微排版素材库，获取 CDN 永久链接。

## 前置读取

从任务目录读取以下文件：

1. **`meta.json`**：获取 `taskDir`、`workId`
2. **`image-progress.json`**：筛选 `status="generated"` 或 `status="bg_removed"` 的条目（即已生成但未上传的图片）

如果没有待上传的图片，直接跳到汇总环节。

## 执行门禁与外传边界

- 仅处理 `status="generated"` 或 `status="bg_removed"` 的当前图片条目
- 上传前应确认用户未取消 Step 8 图片流程
- 只上传当前图片文件或其 `jimengUrl`，不会上传任务目录下其他 JSON 文件

## 数据发送范围（透明披露）

- 文件上传接口：向 `/api/v1/assets/upload` 发送单张图片二进制（`file` 字段）与认证头
- URL 抓取接口：向 `/api/v1/assets/fetch` 发送单个 `jimengUrl` 与认证头
- 两类接口均不上传 `meta.json`、`elements.json`、`template-profile.json` 等任务文件

## 上传逻辑

逐张上传，根据图片状态选择上传方式：

### a) 已去白底（status=bg_removed，localPath 存在）—— 使用文件上传接口

```bash
# 受控执行模板：仅上传当前条目 localPath 指向的单张图片
curl -s --max-time 30 -X POST \
  -H "Authorization: Bearer $WEIPAIBAN_API_KEY" \
  -F "file=@{localPath}" \
  "${WEIPAIBAN_API_BASE:-https://weipaiban.cn}/api/v1/assets/upload"
```

### b) 未去白底或不需透明（status=generated）—— 使用 URL fetch 接口

```bash
# 受控执行模板：仅提交当前条目的 jimengUrl
curl -s --max-time 30 -X POST \
  -H "Authorization: Bearer $WEIPAIBAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"{jimengUrl}"}' \
  "${WEIPAIBAN_API_BASE:-https://weipaiban.cn}/api/v1/assets/fetch"
```

### 响应检查

**必须检查响应**：如果响应包含 `error` 字段（格式为 `{ error: { message, code } }`）或不包含 `data.src` 字段，视为上传失败。

**去重机制**：两个接口均基于文件内容 SHA1 哈希自动去重——相同图片重复上传会直接返回已有记录（HTTP 200），不会产生重复素材，因此重试是安全的。

微排版 Assets API 响应格式详见 [references/api-formats.md](../references/api-formats.md#cdn-上传响应)。

### 逐张上传并更新进度

对每张图片上传后：

1. **如果成功**：
   - 更新 `image-progress.json`：`status` → `"uploaded"`，`cdnSrc` → 响应中的 `data.src`
   - 向用户反馈：
     - 已去白底的：`✅ [{序号}/{总数}] {元素名称}（{分类}）- 已上传 CDN（已去白底）`
     - 未去白底的：`✅ [{序号}/{总数}] {元素名称}（{分类}）- 已上传 CDN`
     - 需透明但去白底失败的：`⚠️ [{序号}/{总数}] {元素名称}（{分类}）- 已上传 CDN（去白底失败，使用原图）`

2. **如果失败**：
   - 更新 `image-progress.json`：`status` → `"failed"`，`error` 设为失败原因
   - 向用户反馈：`❌ [{序号}/{总数}] {元素名称}（{分类}）- 上传失败：{错误原因}，将保留原图`

## 汇总结果

所有图片上传完毕后，展示完整的结果汇总表：

| #   | 元素名称 | 分类   | 需透明  | 结果                                                                                                        |
| --- | -------- | ------ | ------- | ----------------------------------------------------------------------------------------------------------- |
| 1   | {name}   | {分类} | {是/否} | ✅ 已上传 CDN / ✅ 已上传 CDN（已去白底） / ⚠️ 已上传 CDN（去白底失败） / ⏭️ 保留原图 / ❌ 失败（保留原图） |

统计信息：`成功：X 张（其中 A 张已去白底，B 张去白底失败）| 跳过：Y 张 | 失败：Z 张`

## 失败重试

**如果存在失败的图片**：

> ⏸️ **交互点**：有 Z 张图片处理失败。请选择处理方式：
>
> - 「重试」—— 重新处理所有失败的图片
> - 「重试 N」—— 重新处理第 N 张图片
> - 「继续」—— 跳过失败图片（保留原图），继续执行 Step 9
>
> **必须等到用户回复后才能继续。**

对于用户选择重试的图片，根据 `image-progress.json` 中的状态判断从哪步重试：

- `status=pending`（生成就失败了）：回到 Step 8b 的逻辑，重新生成该张
- `status=generated` 且 `needsTransparent=true` 且 `bgRemoved=false`（去背景失败）：重新执行 `rembg i -m u2netp` 处理后上传
- 其他失败（上传失败）：直接在本步骤内重试上传

重试后更新 `image-progress.json` 和汇总表。

**如果所有图片成功或用户选择继续**：

## 后置写入

确认 `image-progress.json` 所有条目状态已最终确定。更新 `meta.json` 的 `currentStep` 为 `"08d"`。然后自动进入 Step 9。
