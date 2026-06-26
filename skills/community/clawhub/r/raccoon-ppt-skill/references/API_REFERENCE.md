# PPT OpenAPI Skill Reference

## 1. Skill 边界

本 skill 只面向以下任务语义：

1. 用户一句话发起 PPT 生成。
2. 在服务端追问时继续收集补充信息。
3. 自动轮询直到返回最终下载链接或失败结果。

本 skill 不向用户暴露内部实现细节（如 `job_id` 等）。

## 2. 最小输入模型

```json
{
  "prompt": "string",
  "role": "string",
  "scene": "string",
  "audience": "string"
}
```

推荐收集策略：

1. 从用户原话直接推断能确定的字段。
2. 对缺失项逐个追问，不一次性问太多。
3. 若用户回答不在推荐枚举内，优先归并到最接近的稳定枚举。
4. 若仍无法匹配，先继续通过自然语言追问，把输入收敛到最接近的稳定枚举。
5. 若确有额外语义需要保留，可把补充说明吸收到 `prompt`，但当前版本不默认生成新的分类值。

## 3. 内部运行时状态

脚本运行时可维护下列字段：

```json
{
  "prompt": "string",
  "role": "string",
  "scene": "string",
  "audience": "string",
  "job_id": "string",
  "status": "queued|running|waiting_user_input|succeeded|failed|canceled",
  "question": "string",
  "download_url": "string",
  "error_message": "string"
}
```

说明：

- `job_id` 仅供脚本内部续跑，不直接给最终用户。
- 如果未来服务端补齐结构化 `*_other_detail`，再扩展 state 结构。
- 前置交互应尽量把用户语义收敛到稳定枚举；当前版本未匹配时应继续前置收集，而不是自动生成新分类。

## 4. 接口定义

鉴权头统一为：

```text
Authorization: Bearer $RACCOON_API_TOKEN
```

接口基地址：

```text
$RACCOON_API_HOST/api/open/office/v2
```

### 4.1 创建任务

```http
POST /api/open/office/v2/ppt_jobs
Authorization: Bearer {token}
Content-Type: application/json
```

请求体：

```json
{
  "prompt": "帮我生成一份介绍 Transformer 发展历程的培训 PPT",
  "role": "研究人员",
  "scene": "培训教学",
  "audience": "大众群体"
}
```

成功响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "job_id": "job_xxx",
    "status": "queued",
    "question": ""
  }
}
```

### 4.2 查询任务

```http
GET /api/open/office/v2/ppt_jobs/{job_id}
Authorization: Bearer {token}
```

成功完成响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "job_id": "job_xxx",
    "status": "succeeded",
    "question": "",
    "download_url": "https://example.com/job_xxx.pptx",
    "error_message": ""
  }
}
```

### 4.3 回复追问

```http
POST /api/open/office/v2/ppt_jobs/{job_id}/reply
Authorization: Bearer {token}
Content-Type: application/json
```

请求体：

```json
{
  "answer": "重点介绍自注意力机制、BERT 和 GPT 的演进关系"
}
```

## 5. 状态机

```text
collect_inputs
  -> create_job
    -> queued/running -> poll
    -> waiting_user_input -> ask_user -> reply_job -> poll
    -> failed -> end_with_error
    -> canceled -> end
    -> succeeded -> return_download_url
```

## 6. 轮询建议

建议脚本采用以下策略：

1. 创建或回复后，先进入约 2 分钟的前台观察窗口。
2. 若任务仍在 `queued/running`，优先结束当前阻塞并保留本地状态。
3. 只有明确需要阻塞等待时，再进入长轮询。
4. 遇到 `waiting_user_input` 立即停止轮询。
5. 遇到 `succeeded`、`failed`、`canceled` 结束。

默认实现可以采用：

- 首次短轮询等待：3 秒
- 常规轮询间隔：5 秒
- 默认最大轮询次数：24

面向 OpenClaw 的建议：

- 默认不要在一次对话里阻塞 30 分钟到 2 小时。
- 创建或回复任务后，先给前台约 2 分钟观察窗口，以便捕获快速返回的 `waiting_user_input` 或早期失败。
- 在本地留存 `job_id -> state_path` 映射，后续通过内部状态文件继续查询。
- 若用户明确要求一直等结果，再切换到长轮询模式。

## 7. 对用户的话术约束

- 解释缺失项时，用自然语言描述 `role`、`scene`、`audience` 的含义。
- 把服务端 `question` 改写成自然追问，不直接甩原始协议字段。
- 返回成功结果时，直接说“PPT 已生成完成，可下载：...”
- 失败时，不要输出堆栈，只给用户可理解的原因。
- 做分类收集时，优先给出贴近稳定枚举的自然语言引导；若没有合适项，继续前置追问并收敛到最接近的稳定枚举。

## 8. 命令行入口约定

建议固定以下命令：

```bash
python3 scripts/main.py auth-check
python3 scripts/main.py create-job --prompt ... --role ... --scene ... --audience ...
python3 scripts/main.py poll-job --job-id ...
python3 scripts/main.py reply-job --job-id ... --answer ...
python3 scripts/main.py list-jobs
python3 scripts/main.py check-job --state-path /abs/path/to/state.json
python3 scripts/main.py find-recent-job --statuses queued,running,waiting_user_input
python3 scripts/main.py generate --prompt ... --role ... --scene ... --audience ...
python3 scripts/main.py generate --prompt ... --resume-state /abs/path/to/state.json
```

其中：

- `generate` 作为统一高层入口，负责创建、回复、轮询和本地 state 持久化。
- `generate` 默认采用短轮询模式，更适合长耗时任务。
- `create-job`、`poll-job`、`reply-job` 作为调试和细粒度操作入口。
- `list-jobs`、`check-job` 用于查看已留存任务。
- `find-recent-job` 用于优先找回最近未完成或最近相关的任务。

## 9. OpenClaw 响应模板

建议按下面几类固定话术响应用户：

### 9.1 已受理，稍后查看

适用状态：

- `queued`
- `running`

推荐话术：

```text
PPT 任务已经受理。前置处理通常会在 2 分钟内完成，但完整生成通常需要 30 分钟到 2 小时。你可以稍后回来，我可以继续帮你查看进度和结果。
```

### 9.2 需要补充信息

适用状态：

- `waiting_user_input`

推荐话术：

```text
继续生成这份 PPT 还需要你补充一点信息：{question}
```

### 9.3 已完成

适用状态：

- `succeeded`

推荐话术：

```text
PPT 已生成完成，可直接下载：{download_url}
```

### 9.4 任务过多

适用场景：

- 创建任务时命中“未完成任务数达到上限”

推荐话术：

```text
你当前已有多个 PPT 任务正在执行，请稍后再试，或先等已有任务完成后再创建新的任务。
```

补充约定：

- 若命中业务错误码 `600020`，应按“当前已有多个任务执行中”处理，不要继续重试建单。
- 若命中业务错误码 `600021`，表示当前状态不允许 `reply`，应提示用户先查看最新状态，不要把它误判成补充问题本身。

### 9.5 失败

适用状态：

- `failed`
- `canceled`

推荐话术：

```text
这次 PPT 任务未能完成：{error_message}
```
