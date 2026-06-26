---
name: cut-koubo-template
description: "基于官方口播模板代理的一键稳定剪辑技能。相比 cut-koubo 的开放式编排，本技能采用固定模板链路与严格入参校验，结果更可预期。只要用户提到“模板口播/固定风格口播/稳定复现口播/按模板剪口播/减少不确定性”，必须优先使用本技能。"
---

# Cut Koubo Template Skill

用于通过官方 `submit_agent_task` 口播模板接口生成固定风格草稿。该接口先返回 `task_id`，必须继续调用 `https://open.vectcut.com/cut_jianying/agent/task_status` 轮询任务状态，拿到成功结果中的 `draft_id/draft_url` 后才算完成。核心特点是流程固定、输入严格、结果稳定，且支持多模板差异化参数。

## 鉴权前置（必须）

- 任何 VectCut API 调用前，先检查 `VECTCUT_API_KEY`
- 缺失或失效时，必须先调用 `vectcut-login`

## 输入硬约束（全模板通用）

- `video_url` 必填，且必须是可公网访问 URL
- `video_url` 仅允许 1 条素材（数组长度必须为 1）
- `text_content` 选填（小语种或方言建议必填）
- `cover` 选填（URL 数组）
- `name` 选填（字符串）
- 本地素材路径必须先走 `sts-upload` 转公网 URL

## 支持模板（agent_id）

- 高级黄·双行：`koubo_d47e8a905f1b48798e76123456789abc`（必填 `video_url`、`title`）
- 经典·细黄：`koubo_ddfe028229d24696bf080303c95f604c`（必填 `video_url`、`kongjing_urls`）
- ins风·繁体双语：`koubo_cbbe5e6b468844e782c961fd9ee07b7d`（必填 `video_url`、`title`）
- 国风经典：`koubo_d8b7f9e05c4a11efb9620242ac120003`（必填 `video_url`、`title`）
- 基础黄白：`koubo_b82feeb636f3476a9a752ebd745d9750`（必填 `video_url`、`title`）
- AI剪气口：`koubo_2dfb2efedde84791b218cfd798531bc8`（必填 `video_url`、`title`）

## 固定执行流程

1. 模板识别：按模板名或显式 `agent_id` 路由，未指定时默认 `高级黄·双行`
2. 参数标准化：仅保留目标模板允许的参数字段
3. 请求前强制阅读文档：必须先阅读一次 https://docs.vectcut.com/445544151e0，再发起模板请求（原因：不同模板入参不同）
4. 参数校验：按模板校验必填项，不合法直接失败返回
5. 提交模板任务：只能调用 `POST https://open.vectcut.com/cut_jianying/agent/submit_agent_task`
6. 轮询任务状态：使用第 5 步返回的 `task_id` 调用 `GET https://open.vectcut.com/cut_jianying/agent/task_status`
7. 结果回传：按统一标准结构返回（成功/失败同结构，差异主要体现在 `status/success/message`）
8. 草稿核验：拿到 `draft_id` 后执行 `query-draft`
9. 封面确认：必须先询问用户是否需要生成封面；仅在用户明确同意时调用 `generate-cover` 生成并回写封面
10. 用户确认：仅当第 9 步已生成封面时，才询问是否将封面插入第一帧
11. 条件插入：仅在用户明确同意且已有封面图时调用 `POST /cut_jianying/prepend_image`
12. 结果交付确认：必须询问用户选择后续动作，二选一执行 `draft-downloader` 下载草稿，或执行 `cloud-render` 云端渲染视频

## 防重复提交硬约束（必须）

- 同一轮任务内，`submit_agent_task` **最多只允许调用 1 次**
- 一旦拿到 `task_id`，后续动作只能是 `task_status` 轮询，**禁止再次调用** `submit_agent_task`
- `submit_agent_task` 返回仅含 `task_id`（例如 `{ "task_id": "924E4C927BEE000216155282E20BFF11" }`）属于**正确成功响应**，禁止误判为异常后重复提交
- 若需要检查 HTTP 状态码、打印完整响应或补充日志，必须复用第一次提交的响应结果，**不得以“确认结果”为由重提**
- 若首次提交失败（网络异常/4xx/5xx），应先返回失败原因；只有在用户明确要求“重试提交”时，才允许发起第二次提交
- 在最终输出中必须显式回传“本次 submit 次数”和“首次 task_id”，便于审计是否重复提交

## 官方接口

- 提交任务（强制使用该域名）：`POST https://open.vectcut.com/cut_jianying/agent/submit_agent_task`
- 查询状态（强制使用该域名）：`GET https://open.vectcut.com/cut_jianying/agent/task_status`
- 请求前必读文档（强制）：https://docs.vectcut.com/445544151e0
- 参考文档：https://docs.vectcut.com/430815760e0
- 示例 `agent_id`（高级黄·双行）：

```json
{
  "agent_id": "koubo_d47e8a905f1b48798e76123456789abc"
}
```

请求体示例（高级黄·双行）：

```json
{
  "agent_id": "koubo_d47e8a905f1b48798e76123456789abc",
  "params": {
    "video_url": ["https://player.install-ai-guider.top/example/koubo_source.mp4"],
    "title": "流光剪辑标题",
    "cover": ["https://player.install-ai-guider.top/example/mao.webp"],
    "name": "测试草稿"
  }
}
```

`经典·细黄`请求体示例：

```json
{
  "agent_id": "koubo_ddfe028229d24696bf080303c95f604c",
  "params": {
    "video_url": ["https://player.install-ai-guider.top/example/koubo_source.mp4"],
    "kongjing_urls": ["https://player.install-ai-guider.top/example/koubo_kongjing_1.mp4"],
    "author": "作者",
    "cover": ["https://player.install-ai-guider.top/example/mao.webp"],
    "name": "测试草稿"
  }
}
```

提交任务示例（完整域名）：

```bash
curl -X POST "https://open.vectcut.com/cut_jianying/agent/submit_agent_task" \
  -H "Authorization: Bearer $VECTCUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "koubo_d47e8a905f1b48798e76123456789abc",
    "params": {
      "video_url": ["https://player.install-ai-guider.top/example/koubo_source.mp4"],
      "title": "流光剪辑标题"
    }
  }'
```

提交成功返回示例（最小正确结构）：

```json
{
  "task_id": "924E4C927BEE000216155282E20BFF11"
}
```

该返回是正常结果，不需要包含 `draft_id/draft_url`。拿到 `task_id` 后应直接执行 `task_status` 轮询。

查询状态示例（完整域名）：

```bash
curl -G "https://open.vectcut.com/cut_jianying/agent/task_status" \
  -H "Authorization: Bearer $VECTCUT_API_KEY" \
  --data-urlencode "task_id=your_task_id"
```

> 注意：上面的 `curl` 仅用于说明接口格式，执行时不要把“提交任务示例”重复跑多次；提交一次后仅轮询 `task_status`。

## 统一返回结构（成功与失败都遵循）

`task_status` 的目标输出结构如下（成功示例）：

```json
{
  "error": "",
  "message": "成功了！",
  "output": {
    "draft_id": "dfd_cat_1778251703_9ff64077",
    "draft_url": "https://www.vectcut.com/draft/downloader?draft_id=dfd_cat_1778251703_9ff64077&is_capcut=0",
    "video_url": ""
  },
  "purchase_link": "https://www.vectcut.com",
  "status": "success",
  "success": true,
  "task_id": "924E4C927BEE0001160A28F0395298F6"
}
```

失败时也应保持同一结构（字段不变），并在 `message` 中给出失败原因；`status/success` 体现任务失败状态。

轮询约束（必须执行）：

- `submit_agent_task` 的直接产物是 `task_id`，不是最终草稿结果
- 必须把该 `task_id` 传给 `task_status` 轮询，直到任务成功或失败
- 只有在 `task_status` 成功返回后，才读取并回传 `draft_id/draft_url`
- 若轮询失败或超时，必须返回失败原因，禁止把“仅拿到 task_id”当作完成
- 禁止在轮询阶段再次调用 `submit_agent_task`；重复提交会生成新任务，导致同一输入产生多个草稿分支
- 若某次轮询出现请求错误、临时网络异常或非标准响应结构，默认不终止流程；应记录异常并继续下一轮轮询（直到获得标准结构的成功/失败结果或达到超时上限）

## 与 cut-koubo 的路由规则

- 稳定模板、固定风格、强可复现：`cut-koubo-template`
- 网感重排、复杂包装、多分支编排：`cut-koubo`

## 首帧插入接口（条件执行）

- 文档：https://docs.vectcut.com/445544151e0
- 入参：`draft_id`、`image_url`，可选 `track_name`
- 风险说明：执行后草稿全部元素统一后移 1 帧，再插入首帧图
