---
name: xingchen-image-api
description: Use the Xingchen AI customer API to create and monitor images for the Xingchen AI website with a customer-owned xk_live API key. Trigger for requests mentioning 星辰AI, 星辰 AI, Xingchen AI, xingchen-image-api, OpenClaw image generation, website API image generation, 商品图, 电商主图, 商品场景图, 海报生图, 参考图生图, 爆款构图复用, 局部重绘, 局部替换, 扩图, 去水印, 高清修复, AI试衣, 换装, 模特背景, 姿势变化, or image task polling through /api/generate and /api/jobs. Do not trigger for 爱创AI/51aic/aicraft integrations, video generation, payment, promotion, account administration, or asset deletion.
license: Proprietary
---

# 星辰 AI 生图 Skill

通过星辰 AI 的顾客 API 调用我们网站现有的电商图片工作流。这个 skill 只负责图片生成和任务查询，不调用爱创 AI、视频、资产删除或支付接口。详细请求字段、响应和错误处理见 [references/api.md](references/api.md)。

## 认证

从运行环境读取 `XINGCHEN_API_KEY`，不要要求用户把密钥贴到公共对话，也不要把密钥写进日志、提示词、图片 URL 或生成结果。密钥应为 `xk_live_...` 格式。

请求地址使用 `XINGCHEN_API_BASE_URL`；没有配置时使用当前部署的站点地址。每次请求发送：

```text
X-Xingchen-API-Key: $XINGCHEN_API_KEY
```

也可使用 `Authorization: Bearer $XINGCHEN_API_KEY`。API 密钥只对图片生成提交和任务查询有效。

## 工作流程

1. 明确用户的图片用途、主体、风格、比例和数量；保留用户原始意图，不擅自改成视频或详情图任务。
2. 选择最接近的网站工作流：普通商品图用 `/studio/image`，爆款构图复用用 `/studio/hot-remake`，局部编辑用 `/studio/local-crop`，高清修复/扩图/去水印使用对应 `/studio/retouch/*`，AI 模特使用对应 `/studio/ai-model/*`。不要把不同工作流混成一个 prompt。
3. 有参考图时，只接受已经可访问的 HTTPS URL。当前顾客 API 密钥不能调用 `/api/assets/upload`；如果用户只有本地文件，应先在网站账户中心上传，或明确告知需要网站上传入口。不要把 base64 图片塞进生成请求。
4. 调用 `/api/generate`，请求体遵循 [references/api.md](references/api.md)。每次生成使用新的 `clientRequestId`，网络重试必须复用同一个 ID。
5. 从响应中的 `job.id` 或 `job.jobId` 取得任务 ID，轮询 `/api/jobs/{jobId}`，直到成功、失败或明确需要重试。
6. 成功后优先展示 `preview`、`thumbnailUrl` 或 `outputs[].preview`；原图 URL 仅作为下载或查看大图链接。不要在对话中直接铺满原图。
7. 失败时展示 API 返回的安全错误消息、任务 ID 和是否扣点状态；不要猜测任务已成功，也不要自动重复提交不同的 clientRequestId。

## 边界

- 不请求、保存或传播爱创 AI 的 Token。
- 不调用 `/api/account/*`、积分充值、支付、推广或后台接口。
- 不把服务端 APIMart 密钥暴露给用户或 skill。
- 不伪造 `cost` 绕过计费；服务端计算最终扣点，skill 只把用户选择的数量、比例、质量和工作流传入。
- 不在没有参考素材的情况下调用必须上传素材的工作流，例如 AI 模特、局部编辑和高清修复。
- 用户未提供 API 密钥时，只说明如何在账户中心生成并配置，不要代用户创建或索取密钥。
- 用户明确要求删除生成资产时，停止并说明本 skill 没有删除权限。
