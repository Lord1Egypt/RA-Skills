# Step 8b：逐张生成图片

根据 Step 8a 构造好的 prompt，逐张调用即梦 API 生成图片。

## 前置读取

从任务目录读取以下文件：

1. **`meta.json`**：获取 `taskDir`
2. **`image-prompts.json`**：每张图的 `prompt`、`negativePrompt`、`ratio`、`needsTransparent`
3. **`image-progress.json`**：确认哪些图片状态为 `pending`（支持断点恢复）

## 处理流程

**处理顺序**：按 `image-prompts.json` 中 `prompts` 数组的顺序，先处理独立 `image` 元素，再处理 `slideshow` 元素中的 `assets` 图片。

**⚠️ 并发限制**：即梦 API 同时只能处理 1 个生成任务，必须严格串行处理，禁止并行。

### 跳过已完成的图片

如果 `image-progress.json` 中某张图片的 `status` 不是 `pending`（断点恢复场景），直接跳过。

### 逐张生成

对每张 `status=pending` 的图片，使用**子代理**处理。子代理的指令极度精简：

> **子代理任务**：生成一张图片并返回 URL。
>
> **前置假定**：`VOLCENGINE_AK` 与 `VOLCENGINE_SK` / `VOLCENGINE_TOKEN`（二选一）已通过 Step 8a 的依赖检测，子代理无需再次校验。
>
> **输入参数**：
>
> - elementId: {元素ID}
> - prompt: "{已构造好的完整 prompt}"
> - negativePrompt: "{排除词}"
> - ratio: {宽高比}
>
> **执行步骤**：
>
> 1. 调用即梦技能，使用上述 prompt 和 ratio 生成图片
> 2. 返回结果：jimengUrl 或 error

**⚠️ 串行约束**：必须等待当前子代理完全返回结果后，才能启动下一个子代理。

### 子代理返回后

子代理返回后，主代理**立即执行**以下操作：

1. **如果成功**：
   - 如果该图片 `needsTransparent=true`，下载图片到本地 `{taskDir}/images/{elementId}_generated.png`（供 Step 8c 使用）
   - 更新 `image-progress.json` 中对应条目：`status` → `"generated"`，`jimengUrl` 设为即梦返回的 URL
   - 向用户反馈：`✅ [{当前序号}/{总数}] {元素名称}（{分类}）- 生成完成`

2. **如果失败**：
   - 更新 `image-progress.json` 中对应条目：`status` → `"failed"`，`error` 设为失败原因
   - 向用户反馈：`❌ [{当前序号}/{总数}] {元素名称}（{分类}）- 生成失败：{错误原因}`

3. 如果后续还有未处理的图片：`🔄 正在处理下一张：{下一张元素名称}...`

**注意**：即梦生成的临时 URL 可能有时效限制。如果 `needsTransparent=true`，必须在生成后立即下载到本地，避免后续 Step 8c 使用 rembg 处理时 URL 已过期。对于不需要透明的图片，URL 将在 Step 8d 直接传给微排版 Assets API。

## 断点恢复

如果 Step 8b 中断后重新执行：

1. 读取 `image-progress.json`，识别 `status=pending` 的条目
2. 仅对这些图片重新生成，已生成的图片（status=generated）不重复处理
3. 向用户展示恢复状态：

```
🔄 检测到上次图片生成未完成，正在恢复...
- 已生成：X 张（复用已生成的图片）
- 待生成：Y 张
- 跳过：Z 张

继续处理剩余图片...
```

## 后置写入

所有图片处理完毕后，确认 `image-progress.json` 已更新所有条目的状态。更新 `meta.json` 的 `currentStep` 为 `"08b"`。然后自动进入 Step 8c。
