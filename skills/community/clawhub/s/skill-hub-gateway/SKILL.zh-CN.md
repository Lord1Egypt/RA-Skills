# Skill Hub Gateway（简体中文）

默认 API 地址：`https://gateway-api.binaryworks.app`

默认站点地址（上传路由）：`https://gateway.binaryworks.app`

英文文档：`SKILL.md`

## 版本检查协议（Agent）

- 官方最新版本来源：`GET /skills/manifest.json` 的 `data.version`。
- 本地当前版本来源：已安装 `SKILL.md` frontmatter 中的 `version`。
- 版本比较规则：使用语义化版本顺序（`major.minor.patch`）。
- 检查频率：会话启动时检查一次；同一会话内最多每 24 小时再检查一次。
- 检查失败（网络/超时/解析错误）时不得阻断运行时调用，继续当前流程并在下一次允许窗口重试。

## 更新决策流程（Agent）

- 当 `latest_version > current_version` 时，Agent 需读取本文档 `Release Notes` 对应版本小节生成 `update_summary`。
- Agent 需向用户展示：
  - `current_version`
  - `latest_version`
  - `update_summary`
- 用户决策选项：
  - `立即更新`
  - `本会话稍后提醒`
- 若用户选择 `本会话稍后提醒`，同一会话内针对同一目标版本不重复提示；新会话可再次提示。

## 首次接入（install_code）

脚本默认会自动完成接入流程：

1. 调用 `POST /agent/install-code/issue`，请求体可用 `{"channel":"local"}` 或 `{"channel":"clawhub"}`。
2. 读取 `data.install_code`。
3. 调用 `POST /agent/bootstrap`，请求体：`{"agent_uid":"<agent_uid>","install_code":"<install_code>"}`。
4. 读取 `data.api_key`，后续通过 `X-API-Key` 或 `Authorization: Bearer <api_key>` 调用。

手工覆盖方式：

- 仍可显式传入 `api_key`。
- 若未传 `agent_uid` 与 `owner_uid_hint`，脚本会基于当前工作目录生成稳定的本地默认值。

## Portal Actions（用户闭环）

动作目录（单 Skill，多动作）：

- `portal.me` -> `GET /user/me`
- `portal.balance` -> `GET /user/points/balance`
- `portal.ledger.query` -> `GET /user/points/ledger`
- `portal.usage.query` -> `GET /user/usage`
- `portal.skill.execute` -> `POST /user/skills/execute`
- `portal.skill.poll` -> `GET /user/skills/runs/:runId`
- `portal.skill.presentation` -> `GET /user/skills/runs/:runId/presentation`
- `portal.voucher.redeem` -> `POST /user/vouchers/redeem`（写操作）
- `portal.recharge.create` -> `POST /user/recharge/orders`（写操作）
- `portal.recharge.get` -> `GET /user/recharge/orders/:orderId`

写操作门禁：

- `portal.voucher.redeem`、`portal.recharge.create` 必须 `payload.confirm === true`。
- 缺少确认时本地直接拒绝，不向后端发写请求。

## Payload 约定

默认输入约定：

- `payload.input` 是 `portal.skill.execute` 的主输入对象。
- `payload.request_id` 可选，原样透传。
- 查询动作直接读取 `payload` 查询参数（`date_from`、`date_to`、`service_id`、`channel`）。

附件归一化约定：

- 优先使用显式 URL 字段：`image_url`、`audio_url`、`file_url`。
- 存在 `attachment.url` 时，自动映射到能力目标字段。
- 存在 `file_path` 时，自动走 `{site_base}/api/blob/upload` 上传并回填 URL；当运行环境缺少 `@vercel/blob/client` 时会自动回退到 `{site_base}/api/blob/upload-file`。
- 若 agent 运行环境缺少 `@vercel/blob/client`，也可以先由业务后端完成媒体预上传（例如 Vercel Blob），再传 `attachment.url` 或显式 URL 字段执行。
- `site_base_url` 为受控字段：运行时仅接受可信站点基址（默认 `https://gateway.binaryworks.app` 或环境变量 `SKILL_SITE_BASE_URL`）。
- 正常产品链路下，不应要求用户手工粘贴媒体 URL。

Presentation 文件输出：

- `portal.skill.presentation` 支持可选 `include_files=true`，返回 `visual.files.assets` 渲染结果文件 URL。
- `portal-action.mjs` 在调用 `portal.skill.presentation` 时默认 `include_files=true`（除非显式关闭）。
- 图像类输出包含 `overlay`（标注图），并在有分割/抠图结果时返回 `mask` / `cutout` 文件。
- 音频类输出会在 `output.media_files.assets` 中返回上传后的文件 URL（需配置 blob 存储）。

## 鉴权桥接（api_key -> user session）

用户动作使用固定桥接路径：

1. 先得到运行时上下文（`api_key`、`agent_uid`、`owner_uid_hint`、`base_url`）。
2. 使用 `X-API-Key` + `x-agent-uid` 调 `GET /agent/me` 获取 `user_id`。
3. 使用 `user_id + api_key` 调 `POST /user/api-key-login` 获取 `userToken`。
4. 后续 Portal Action 使用 `Authorization: Bearer <userToken>` 调用。

## 积分不足恢复

当返回 `POINTS_INSUFFICIENT` 时：

- 保留 `error.code` 与 `error.message`。
- 透传 `error.details.recharge_url`（若存在）。
- 诊断信息建议优先执行 `portal.recharge.create` 或直接打开 `recharge_url`。

## 打包脚本

- `scripts/execute.mjs`：`[api_key] [capability] [input_payload] [base_url] [agent_uid] [owner_uid_hint]`
- `scripts/poll.mjs`：`[api_key] <run_id> [base_url] [agent_uid] [owner_uid_hint]`
- `scripts/feedback.mjs`：`[api_key] [payload_json] [base_url] [agent_uid] [owner_uid_hint]`
- `scripts/telemetry.mjs`：共享 best-effort telemetry 上报逻辑
- `scripts/runtime-auth.mjs`：共享自动 bootstrap 逻辑
- `scripts/portal-auth.mjs`：`api_key -> user session` 桥接
- `scripts/portal-action.mjs`：`[api_key] <action> <payload_json> [base_url] [agent_uid] [owner_uid_hint]`
- `scripts/attachment-normalize.mjs`：附件 URL/本地路径归一化与自动上传

## Telemetry 与反馈

- 随包脚本已支持 best-effort telemetry 上报，覆盖 auth/execute/poll/feedback 场景。
- telemetry 上报失败不会改变主流程退出语义，仅输出 stderr 结构化日志。
- 可选环境变量：
  - `SKILL_TELEMETRY_ENABLED`（默认 `true`）
  - `SKILL_TELEMETRY_BASE_URL`（默认复用运行时 `base_url`）
  - `SKILL_TELEMETRY_TIMEOUT_MS`（默认 `2000`）
- `feedback.mjs` 会调用 `POST /feedback/submit`，并在 `metadata` 中附带 `agent_uid` 与 `owner_uid_hint`。

## 能力 ID

- `human_detect`
- `image_tagging`
- `tts_report`
- `embeddings`
- `reranker`
- `asr`
- `tts_low_cost`
- `markdown_convert`
- `face-detect`
- `person-detect`
- `hand-detect`
- `body-keypoints-2d`
- `body-contour-63pt`
- `face-keypoints-106pt`
- `head-pose`
- `face-feature-classification`
- `face-action-classification`
- `face-image-quality`
- `face-emotion-recognition`
- `face-physical-attributes`
- `face-social-attributes`
- `political-figure-recognition`
- `designated-person-recognition`
- `exhibit-image-recognition`
- `person-instance-segmentation`
- `person-semantic-segmentation`
- `concert-cutout`
- `full-body-matting`
- `head-matting`
- `product-cutout`

## Release Notes

发布新版本时请在此追加小节。Agent 面向用户展示的更新摘要必须基于本区块生成。

### 2.4.2（2026-03-12）

**What's New**

- 新增 `/api/blob/upload-file` 直传兜底：当 `@vercel/blob/client` 缺失时用于 `file_path` 上传。
- `portal.skill.presentation` 新增文件渲染输出（`visual.files.assets`），返回标注图/掩膜/抠图 URL。
- 音频输出统一归一化为 `output.media_files.assets`，并上传为可访问文件 URL（需配置 blob 存储）。

**Breaking/Behavior Changes**

- 无。

**Migration Notes**

- 在缺少 `@vercel/blob/client` 的环境下，仍可直接传 `file_path`，运行时会自动回退到直传接口。
- 如需拿到渲染文件，请使用 `portal.skill.presentation` 并设置 `include_files=true`。

### 2.4.1（2026-03-12）

**What's New**

- 为 `portal.skill.execute` 增加服务端 `attachment.url` 归一化（同时支持 `input.attachment.url` 与顶层 `attachment.url`）。
- 明确并实现显式媒体 URL 优先级：当 `image_url`/`audio_url`/`file_url` 与 `attachment.url` 同时存在时，优先使用显式 URL。
- 新增端到端测试，覆盖 upload-first 场景与优先级回归。
- 补充缺少 `@vercel/blob/client` 时的兜底建议：先由业务后端预上传，再传 URL 执行。

**Breaking/Behavior Changes**

- 无。

**Migration Notes**

- 现有 `portal-action.mjs` 调用方式保持兼容。
- 在受限 agent 运行环境中，建议将本地文件流程改为“后端预上传 + URL 执行”。

### 2.4.0（2026-03-12）

**What's New**

- 新增用户闭环 `Portal Actions` 契约（账户查询、执行/轮询、券兑换、充值下单/查单）。
- 写操作新增本地双确认门禁：`portal.voucher.redeem`、`portal.recharge.create` 需 `confirm=true`。
- 新增 `portal-auth.mjs`，实现 `api_key -> user session` 鉴权桥接。
- 新增 `portal-action.mjs` 与 `attachment-normalize.mjs`，支持 `attachment.url` 与 `file_path` 自动上传回填。
- 统一积分不足诊断，保留并透传 `recharge_url`。

**Breaking/Behavior Changes**

- 写操作若缺少 `confirm=true` 会本地快速失败。

**Migration Notes**

- 原有 `execute.mjs`、`poll.mjs` 行为保持不变。
- 用户闭环能力建议改用 `portal-action.mjs`。

### 2.3.4（2026-03-11）

**What's New**

- 在运行时脚本中新增 best-effort telemetry 上报，覆盖 auth/execute/poll。
- 新增 `scripts/feedback.mjs`，支持通过 runtime auth（`X-API-Key`）提交结构化反馈。
- 新增共享 telemetry 助手脚本与 `SKILL_TELEMETRY_*` 可选配置。

**Breaking/Behavior Changes**

- 无。

**Migration Notes**

- 现有 execute/poll 调用方式保持不变。
- 若运行环境有出站限制，请放行可选 telemetry 上报端点：`/agent/telemetry/ingest` 与 `/telemetry/ingest`。
