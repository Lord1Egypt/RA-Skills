# 发布已生成素材到小红书

仅当用户明确要求发布到小红书时读取并执行。生成、编辑、下载或展示素材均不构成发布授权，不自动接续发帖。发布无需再次生成素材，不额外收取生成费用。

## 账号与权限

- 用户使用创建 API Key 的同一个平台账号登录[媒体工作台](https://ai-skills.open-idea.net/dashboard/products/spark-media?tab=image)，点击“管理小红书账号”，填写自定义账号备注及完整 Cookie，点击“绑定账号”。显示“已绑定”和账号备注后即可使用；需要更换 Cookie 或账号时，在同一弹窗点击“解绑账号”后重新绑定。Cookie 的获取步骤见弹窗中的“如何获取自己的 Cookie”。
- Cookie 由平台加密保存，不回显；OpenClaw 或其他 Agent 只配置该平台账号的 API Key，无需配置 `XHS_COOKIE`。Cookie 失效时由用户回到工作台更新绑定。
- Agent 不索取、不接收、不记录、不转发 Cookie；不得要求用户在对话中粘贴 Cookie，也不得在 API 请求中传递它。账号查询只返回绑定状态及备注，不返回 Cookie。
- 使用平台 API Key；受限 Key 需具有 `xiaohongshu.account.read`、`xiaohongshu.publish`、`xiaohongshu.read` 对应权限。按现有 API 密钥参考读取环境变量，不显示密钥。
- 先调用 `GET /api/v1/spark-media/xiaohongshu/account`。未绑定时给出网页登录配置入口，待用户完成后重新查询；发布环境不可用时停止提交并如实告知。

## 素材与发布确认

只接受当前用户已成功完成的 `text_to_image`、`image_to_image`、`text_to_video` 或 `image_to_video` 任务 `task_id`；不接受任意链接、文件或他人任务。同步图片生成响应也提供 `task_id`。图片笔记包含该任务的全部生成图片，视频笔记使用该任务已有的视频。

在提交前核对账号备注、完整素材、标题、正文和可见范围。标题 1–20 字，正文最多 1000 字。`is_private` 默认 `true`（私密）；只有用户明确要求公开时设置 `false`。用户明确授权的发布请求可直接执行；若缺少内容或公开意图不明确，则先补齐必要信息。`publish_confirmed=true` 只代表已经获得这次实际发布授权，不可替用户默认确认。

## 提交与查询

`POST /api/v1/spark-media/xiaohongshu/publications`，请求头为 `Authorization: Bearer <平台 Key>`、`Content-Type: application/json` 和必填 `Idempotency-Key: <本次发布的 UUID>`。示例使用已有任务编号，不会创建新的媒体生成任务：

```json
{
  "task_id": "已有的本人成功媒体任务编号",
  "title": "旅途中的光影",
  "description": "经用户核对的笔记正文",
  "is_private": true,
  "publish_confirmed": true
}
```

接受后返回 HTTP 202 与 `publication_id`、`task_id`、`status`、`note_url`、`message`、`terminal`。保留发布编号，使用 `GET /api/v1/spark-media/xiaohongshu/publications/{publication_id}` 查询原发布；查询不会再次发帖。

相同逻辑发布复用原 `Idempotency-Key` 与完全相同输入；不得因工作台/API 入口不同或响应慢而更换 Key 重复提交。同一 Key 改变内容会被拒绝。需要修改笔记时先核对原发布是否已经发出，不把修改视为对结果不确定任务的自动重试。

## 已确认失败后的明确重试

仅当原发布状态为 `failed`（发布前已确认失败、尚未发帖），且用户明确要求重试时，才可提交相同任务和笔记内容的新发布请求。先核对当前绑定账号，使用一个**新的** `Idempotency-Key`，请求中保留 `publish_confirmed=true` 并增加 `retry_failed=true`。服务会创建新的发布编号，保留原失败记录；不要重新生成媒体。工作台可刷新原发布页，核对后点击“重试发布”。

`retry_failed` 不是一般网络重试开关。`queued`、`preparing`、`publishing`、`indeterminate`、查询超时或状态未知时，只能继续查询原发布并核对，不得自动重试发帖或更换 Key 重发。`succeeded` 不重发；已明确发出的笔记另行按用户意图处理。

## 有限等待与结果解释

每 5 秒查询一次，最多查询 60 次或等待 5 分钟；连续 3 次查询失败即停止自动等待。只续查原发布，不自动重复提交。

- `queued`、`preparing`、`publishing`：仍在处理，不宣称成功。
- `succeeded`：平台已取得可验证笔记编号，交付 `note_url` 和可见范围。私密笔记仍为私密，不宣称公开可见。
- `failed`：发布前已确定失败，如实报告 `message`；仅在用户明确要求时，按上述规则使用新 Key 和 `retry_failed=true` 创建重试，不自动重新生成或更换账号提交。
- `indeterminate`：可能已经发出，立即停止自动重试；交付发布编号和最后状态，引导用户到小红书核对账号笔记。无有效笔记编号不能伪报成功。

达到等待上限、网络超时或状态查询中断时，保留 `publication_id`、`task_id`、最后状态和查询路径，说明可以稍后继续查询或刷新工作台页面；不推断成功或失败，不新建发布任务。账号更新或解绑后，原排队任务可能被拒绝；先核对原任务状态和目标账号。
