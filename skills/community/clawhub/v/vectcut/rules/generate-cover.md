---
name: generate_cover
description: "为草稿生成封面并回写：严格按 query_script -> 智能截图 -> 提示词润色 -> submit_task/generate(基于截图图生图) -> modify_draft 推进。用户提到“生成封面/改草稿封面”时必须使用本技能，生图前必须先读取 references 提示词库并完成 prompt 润色。封面任务通常耗时较长，轮询需按长任务处理（通常约10分钟），禁止因短轮询提前判失败。"
---

# Generate Cover Skill

用于“基于已有草稿”生成封面图并回写到草稿。

核心链路为（按顺序）：
1. `query_script`：读取草稿内容与素材结构
2. `submit_video_capture_task`：从第1步提取搜索关键词，去主轨视频智能截图
3. `prompt polish`：根据草稿语义 + 参考提示词库，先润色生成封面提示词
4. `submit_task/generate`：基于第2步截图 URL + 第3步润色 prompt 发起图生图请求
5. `modify_draft`：把第4步得到的封面图 URL 回写到草稿

## 官方接口（必须引用）

- `query_script`：https://docs.vectcut.com/386764616e0
- `submit_video_capture_task`：https://docs.vectcut.com/426656778e0
- `submit_task/generate`：https://docs.vectcut.com/443760774e0
- `modify_draft`：https://docs.vectcut.com/429210482e0

## 关键原则（必须遵守）

- 不要写代码，不要创建脚本，不要函数封装执行。
- 必须分步思考，每一步完成后再决定下一步输入。
- 不允许“自动喂给下一步”式固定拼接；要基于上一步实际输出内容做判断。
- 若上一步信息不足，先补充必要字段再进入下一步。
- 调用 `task_status` 轮询时必须打印进度日志（至少包含 task_id、status、progress/轮询次数）。
- 封面相关异步任务默认按“长任务”执行：建议总轮询窗口不少于 `10` 分钟（推荐 `12-15` 分钟），不要用短超时提前判定失败。
- `submit_task/generate` 的 `prompt` 必须先做润色，不可直接复用草稿原始字段、文件名、JSON 片段。
- 提示词风格参考必须读取：`references/cover_prompt_references.md`
- 封面默认是“海报型封面”：必须包含标题文案与文字排版要求（主标题/副标题/角标至少其一）。
- 仅当用户明确要求“纯画面无字”时，才允许在 prompt 里使用 `no text`。
- 提示词生成采用“参考模板优先”策略：先选一条最匹配的参考提示词作为母版，再做最小必要替换，不重写整段。
- 允许替换的内容仅限：`主题对象`、`场景细节`、`主标题/副标题/角标`、`品牌词/时间信息`；其余风格描述尽量保留母版表达。
- 母版选择改为“随机抽样”：每次从 `references/cover_prompt_references.md` 的参考列表中随机选 1 条，禁止默认固定使用参考1。
- 人物口播封面必须“人物主体高保真”：人物面部、发型、服饰、肤质保持真实质感；风格化只作用于背景、装饰元素与版式，不得把人物本体卡通化或过度风格化。

## 前置条件

- 环境变量 `VECTCUT_API_KEY` 可用
- 若缺失或失效，先调用 `vectcut-login`
- 封面尺寸使用 `9:16`（ `1440x2560`）
- 模型使用`nano_banana_2`

## 五步思考指引

### 第一步：`query_script`（先理解）
- 输入最小集：`draft_id`
- 重点读取：文案主标题、卖点语义、视频素材可用 URL（如 `materials.videos[].remote_url`）
- 产出结论：封面主题句、1-2个卖点、`search_sentence`（搜索关键词）、主轨 `video_url`
- 文案抽取：从草稿文本里整理 `headline`（主标题）、`subheadline`（副标题）、`badge/corner`（角标短句）

### 第二步：`submit_video_capture_task`（去主轨截图）
- 必填：`video_url`、`search_sentence`
- 若接口返回 `task_id`，继续轮询 `task_status` 直到 `success/failed`
- 轮询策略：按长任务窗口执行（建议 `timeout>=600s`，推荐 `720-900s`）
- 若接口直接返回 `image_url`，也要记录截图结果并进入第3步
- 输出检查：必须拿到可访问 `image_url`，否则补充关键词后重试截图

### 第三步：`prompt polish`（新增，先润色再生图）
- 输入：第1步主题结论 + 第2步截图场景 + `references/cover_prompt_references.md`
- 输出：一条“可执行画面语言”的最终 prompt（避免口水词、堆砌词、原始结构字段）
- 润色方法：先从 references 的候选母版里随机抽 1 条，再仅替换草稿关键内容，不做大幅改写
- 推荐结构：`母版风格主体保留 + 草稿关键内容替换 + 标题文案排版落位 + 吸睛目标`
- 文案排版默认必填：`主标题内容 + 副标题内容 + 角标内容(可选) + 字体风格 + 字号层级 + 摆放位置`
- 若草稿有原始文本，优先清洗后复用为标题文案；若文本不足，基于主题自动补一条短标题与副标题
- 只有用户明确要求无字封面时，才写 `no text`
- 口播人物约束必填：在最终 prompt 明确写入“人物主体保持写实高保真、背景与图形可风格化”，避免人物被美漫化/插画化
- 输出时补充“替换清单”：说明本次从母版替换了哪些字段，便于用户校验

### 第四步：`submit_task/generate`（基于截图图生图）
- 必填：`prompt`、`reference_image`
- 推荐：`model=nano_banana_2`、`size=1440x2560`、`compose_draft=false`
- `reference_image` 必须使用第2步截图得到的 `image_url`
- 若返回 `task_id`，继续轮询 `task_status` 直到 `success/failed`
- 轮询策略：生图默认是慢任务，建议 `timeout>=600s`，推荐 `900s`（约 10-15 分钟）
- 输出检查：确认结果里存在可用 `image` URL，再进入第5步

### 第五步：`modify_draft`（最后回写）
- 必填：`draft_id`、`cover`
- `cover` 必须使用第4步成功返回的图片 URL
- 输出检查：确认返回 `success=true` 且有 `draft_url`

## 轮询日志规范（必须输出）

- 每次轮询必须打印：`[poll] api=<name> task_id=<id> status=<status> progress=<progress>`
- 若接口无 `progress` 字段，至少打印：`status` + `poll_count`
- 当状态长期停在 `processing`（例如 30%）时，仍按长任务窗口继续轮询，达到超时窗口后再判定失败
- 结束时必须打印：`[poll-end] status=success|failed` 与关键结果摘要（`image_url` 或 `error`）

## 执行方式

- 按链路顺序执行，不做代码实现。
- 每一步先“读输出并理解”，再“决定下一步输入”。
- 发现字段缺失时先补信息，不要硬进入下一步。
- 在调用 `submit_task/generate` 前，先读取 `references/cover_prompt_references.md`，基于草稿语义完成 prompt 润色。

## 输出

- 第1步理解结论（标题/卖点/关键词/主轨URL）
- 第2步截图结果（`image_url`、`timestamp` 或失败原因）
- 第3步润色后的最终 prompt（必须包含“随机选中的参考母版 + 替换清单 + 主标题/副标题/角标与排版位置 + 人物高保真约束”）
- 第4步生成结果（图片 URL）
- 第5步回写结果（`draft_id`、`draft_url`）
