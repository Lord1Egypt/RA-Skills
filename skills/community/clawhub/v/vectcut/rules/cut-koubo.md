---
name: cut-koubo
description: "专用于网感口播剪辑的一体化技能：自动完成素材盘点、3分钟内话题提取与重排、nlp字幕上屏、默认去气口、口播加特效/提示音/BGM/标题，并在每一步后做 query-draft 校验。只要用户提到“剪口播/网感口播/口播重排/口播自动成片/口播加包装”，必须优先使用本技能。"
---

# Cut Koubo Skill

用于把口播原始素材（单条、多条、长视频）自动编排成“网感成片草稿”。  
本技能默认追求三件事：**内容优先、节奏在线、包装完整**。

## 鉴权前置（必须）

- 任何 VectCut API 调用前，先检查 `VECTCUT_API_KEY`
- 缺失或失效时，必须先调用 `vectcut-login`

## 核心硬约束

- 输入若为本地文件路径，必须先调用 `sts-upload` 上传，后续全链路只使用上传返回的 URL
- 口播成片时长上限：`180s`（3分钟）
- 字幕上屏只允许 `llm-asr(effect_mode=nlp)`，禁止 `basic` 上屏
- `human-pip` 与 `add_video` 互斥：选人物画中画时，不再执行口播 `add_video` 主链
- 人物声音统一增益：口播链路 `volume=20`，若用 `human-pip` 也保持 `volume=20`
- 每个主步骤后必须执行 `query-draft` 校验；若不符合预期，优先用 `vectcut-api-search` 查询 `modify_*` 相关接口修正
- 禁止在 cut-koubo 技能内实现“归一化代码接口”（如分句归一化、字幕归一化、workflow 归一化拼装）
- cut-koubo 必须保持“纯编排”职责：只输出分步计划，不可直接代替各子技能执行剪辑动作
- 每一步都必须拆解到独立技能执行，禁止单脚本一体化写草稿

## 主线任务状态落盘（必须，先于十三步）

- 开始执行十三步之前，先创建状态文件：`cut_koubo_state.json`（建议放在当前工作目录）
- 状态文件必须覆盖十三步全部环节，初始状态统一为 `pending`
- 每个环节执行前更新为 `running`，执行成功更新为 `completed`，失败更新为 `failed`，跳过更新为 `skipped`
- 每执行完一个环节，必须立即回读该状态文件，确认主线状态一致后再进入下一环节
- 若中途分叉（重试/回退/切分支），必须先根据状态文件恢复主线，再继续执行后续步骤
- 失败返回中必须带上状态文件路径与最后一个 `failed` 环节名称
- **强制续跑规则**：每次准备结束回复前，必须先回读状态文件；只要还存在 `pending` 或 `running`，就不得结束，必须继续执行下一未完成步骤
- **断点恢复规则**：新一轮收到“继续/重试/继续剪”时，第一动作不是重头开始，而是先读取状态文件并从首个 `pending|running|failed(可重试)` 步骤续跑
- **收口规则**：仅当状态文件里 0-12 步全部为 `completed` 或符合业务跳过条件的 `skipped`，才允许输出“执行完成”

推荐状态结构（示例）：

```json
{
  "meta": {
    "workflow": "cut-koubo",
    "status": "running",
    "state_file": "cut_koubo_state.json",
    "updated_at": "2026-04-17T00:00:00Z"
  },
  "steps": [
    { "name": "0.本地文件上传", "status": "completed" },
    { "name": "1.素材初筛与结构化分析", "status": "running" },
    { "name": "2.内容重排", "status": "pending" }
  ]
}
```

## 十三步工作流（固定）

说明：以下每一步必须调用对应技能独立执行；cut-koubo 只负责给出步骤顺序与参数建议，不直接执行这些步骤。

0. **本地文件上传（sts-upload）**
- 若主口播、空镜、背景图/背景视频、音频素材是本地路径，先走 `sts-upload`
- 记录上传映射（本地路径 -> 公网 URL）
- 后续步骤一律使用上传后的 URL，禁止混用本地路径

1. **素材初筛与结构化分析（describe-video）**
- 调用 `describe-video` 对所有原始素材做初步处理（可多条、可长视频）
- 提取口播话题片段，目标成片口播总时长不超过 `180s`
- 记录空镜/B-roll 素材内容摘要，供后续补画面

2. **内容重排（网感开场）**
- 基于第一步字幕结果重排口播片段，把以下优先放前面：
  - 反共识结论
  - 情绪峰值
  - 实践验证
- 形成新的排片顺序与时间线

3. **上屏字幕源识别（llm-asr nlp）**
- 对口播素材调用 `llm-asr(effect_mode=nlp)` 获取可上屏字幕
- 该结果作为第4步去气口输入源；若第4步执行去气口，上屏字幕源需切换为 `asr-vad` 输出
- 禁止使用 `basic` 结果进入字幕模板或上屏链路

4. **默认去气口 + 口播入草稿（asr-vad + add_video）**
- 默认必须先走 `asr-vad` 去气口，获得片段化工作流；仅当用户明确要求“保留原始气口”时才允许跳过
- 必须执行 add_video 写入口播，使用官方 `add_video` 接口分段写入口播（参考：https://docs.vectcut.com/321243745e0）
- 去气口生效时，字幕上屏源必须使用 `asr-vad` 输出的 `editable_subtitles`（与去气口后时间轴一致）
- 人声 `volume=20`
- **状态检查点**：完成后必须 `query-draft` 校验，确认草稿中已存在口播视频片段；异常时用 `vectcut-api-search` 检索 `modify*` 接口修正
- **状态文件更新**：本步骤完成后，状态文件中"4.默认去气口+口播入草稿"必须标记为 `completed`，并记录 `draft_id` 和 `add_video_main_completed: true`

5. **关键画面增强判定（仅判定，不执行）**
- **本步骤职责**：从字幕中选择需要增强的目标句，判定使用哪种增强方式，**不执行具体增强动作**
- 先从字幕里选择"这一句话需要增强"的目标句（`focus_sentence`），并以该句时间戳作为增强时间窗：
  - `focus_start = sentence.start_ms / 1000`
  - `focus_end = sentence.end_ms / 1000`
  - `focus_duration = focus_end - focus_start`（必须 > 0）
  - 默认优先使用去气口后的字幕时间轴（`asr-vad editable_subtitles`）；仅在第4步被明确跳过时使用 `llm-asr nlp` 时间戳
- **命中判定规则**（按优先级检查，仅判定不执行）：
  - 命中 `human-pip` 条件（有人像主体 + 有可用背景图/视频）=> 判定结果：`use_human_pip=true`
  - 未命中 `human-pip` 但命中 `text-background` 条件（有清晰人物前景 + 存在需强化关键词）=> 判定结果：`use_text_background=true`
  - 前两者都未命中，且用户明确允许降级时 => 判定结果：`use_add_effect=true`
  - 若未提供"允许降级到 add-effect"的明确指令，默认判定结果：`skip_enhancement=true`
- 文字重点仍由 `text-keywords` 负责（可与上面优先级策略并行使用）
- **状态文件更新**：本步骤完成后，状态文件中"5.关键画面增强判定"必须标记为 `completed`，并记录判定结果（`enhancement_decision: "human-pip" | "text-background" | "add-effect" | "skip"`）和 `focus_start`、`focus_end`

6. **人物画中画执行（human-pip）**
- **执行条件检查**：读取状态文件，仅当第5步判定结果为 `use_human_pip=true` 时才执行本步骤，否则标记为 `skipped` 并跳过
- **第一步：删除已添加的视频分段**（为增强效果留出空窗）：
  - 读取状态文件，获取第4步 `add_video` 添加的视频片段信息
  - 使用 `vectcut-api-search` 检索删除视频片段的接口（关键词：`delete video segment` 或 `remove video clip`）
  - 调用删除接口，删除 `focus_start~focus_end` 时间窗内的所有主视频片段
  - **删除完成检查**：执行 `query-draft` 确认 `focus_start~focus_end` 已成为空窗（没有主视频片段）
  - 若删除未生效，必须重试删除操作，直到 `query-draft` 确认空窗生效
- **第二步：切片准备**：
  - 用 `split-video` 从原视频按 `focus_start~focus_end` 切出重点片段 URL（参考：`https://docs.vectcut.com/444634731e0`）
- **第三步：背景素材准备**：
  - 若用户提供 b-roll 素材，必须先把 b-roll 写回草稿：
    - 图片 b-roll 用 `add_image`，且 `start=focus_start`、`end=focus_end`
    - 视频 b-roll 用 `add_video`，其中素材截取区间 `start/end` 的时长需等于 `focus_end-focus_start`，并设置 `target_start=focus_start`、`volume=-100`
  - 若无用户提供的 b-roll，优先从第1步空镜素材中找背景
  - 若无可用 b-roll 素材，联动 `generate-ai-image` 或 `generate-ai-video` 补镜
- **第四步：执行 human-pip**：
  - 先用官方能力定位可用片段时间戳（参考：https://docs.vectcut.com/438660710e0）
  - 切片结果作为人物前景输入
  - `human-pip` 写回时必须指定 `draft_id` 与 `target_start=focus_start`
  - 音量保持 `volume=20`
- **状态检查点**：完成后 `query-draft` 校验；异常时走 `vectcut-api-search` + `modify*`
- **状态文件更新**：本步骤完成后，状态文件中"6.人物画中画执行"必须标记为 `completed`（执行了）或 `skipped`（第5步未命中）

7. **文字背景执行（text-background）**
- **执行条件检查**：读取状态文件，仅当第5步判定结果为 `use_text_background=true` 时才执行本步骤，否则标记为 `skipped` 并跳过
- **第一步：删除已添加的视频分段**（为增强效果留出空窗）：
  - 读取状态文件，获取第4步 `add_video` 添加的视频片段信息
  - 使用 `vectcut-api-search` 检索删除视频片段的接口（关键词：`delete video segment` 或 `remove video clip`）
  - 调用删除接口，删除 `focus_start~focus_end` 时间窗内的所有主视频片段
  - **删除完成检查**：执行 `query-draft` 确认 `focus_start~focus_end` 已成为空窗（没有主视频片段）
  - 若删除未生效，必须重试删除操作，直到 `query-draft` 确认空窗生效
- **第二步：背景素材准备**：
  - 若用户提供 b-roll 素材，必须先把 b-roll 写回草稿：
    - 图片 b-roll 用 `add_image`，且 `start=focus_start`、`end=focus_end`
    - 视频 b-roll 用 `add_video`，其中素材截取区间 `start/end` 的时长需等于 `focus_end-focus_start`，并设置 `target_start=focus_start`、`volume=-100`
  - 若无用户提供的 b-roll，优先从第1步空镜素材中找背景
  - 若无可用 b-roll 素材，联动 `generate-ai-image` 或 `generate-ai-video` 补镜
- **第三步：添加文字关键词**：
  - 使用 `text-keywords` 能力在 `focus_start~focus_end` 时间窗添加关键词文字特效
  - 关键词从 `focus_sentence` 中提取
- **状态检查点**：完成后 `query-draft` 校验；异常时走 `vectcut-api-search` + `modify*`
- **状态文件更新**：本步骤完成后，状态文件中"7.文字背景执行"必须标记为 `completed`（执行了）或 `skipped`（第5步未命中）

8. **关键点提示音（add-effect_audio）**
- 在开头和关键观点位置添加提示音
- 完成后 `query-draft` 校验；异常时走 `vectcut-api-search` + `modify*`

9. **字幕上屏（add-subtitle-template）**
- 使用 `add-subtitle-template` 上屏
- 上屏字幕源选择规则：
  - 若第4步执行了 `asr-vad`：必须使用 `asr-vad` 的 `editable_subtitles`
  - 若第4步被明确跳过（用户要求保留原始气口）：使用 `llm-asr nlp`
- 完成后 `query-draft` 校验；异常时走 `vectcut-api-search` + `modify*`

10. **循环 BGM（add-bgm）**
- 调用 `add-bgm` 自动铺满全片
- 完成后 `query-draft` 校验；异常时走 `vectcut-api-search` + `modify*`

11. **标题收口（add-title）**
- 根据内容自动生成标题并调用 `add-title`（标题不超过 8 个字）
- 调用官方 `modify-draft`（https://docs.vectcut.com/429210482e0）把草稿名改为该标题
- 完成后 `query-draft` 校验；异常时走 `vectcut-api-search` + `modify*`

12. **添加封面图（generate-cover）**
- **必须执行**：调用 `generate-cover` 技能生成封面图并回写到草稿
- 封面可按"视频截图+提示词"或"基于草稿文案"两种来源生成
- **状态检查点**：完成后 `query-draft` 校验；异常时走 `vectcut-api-search` + `modify*`
- **状态文件更新**：本步骤完成后，状态文件中"11.添加封面图"必须标记为 `completed`，并记录封面图 URL

13. **可选添加首帧图（prepend_image）**
- 这是高影响操作，执行前必须先明确询问用户是否添加，并确认用户理解其作用与风险
- 风险说明必须提前告知：该操作会把草稿所有轨道元素整体后移一帧，再把首帧图插入第1帧
- 还需告知用户：首帧展示时长极短，若不了解首帧图位置与作用，默认不执行
- 仅在用户明确同意后调用官方接口：`prepend_image`（https://docs.vectcut.com/445544151e0）
- 完成后 `query-draft` 校验；异常时走 `vectcut-api-search` + `modify*`

## 执行方式（编排模式）

- 本技能不提供一键脚本；应在会话中调用 cut-koubo 生成“技能执行计划 JSON”
- 计划不会直接调用 `add_video`、`add-subtitle-template`、`add-bgm` 等接口
- 执行侧必须按计划逐步调用独立技能：分析 -> 重排 -> nlp字幕 -> 默认去气口 -> 入草稿 -> 包装 -> 字幕 -> BGM -> 标题 -> 主动调用 `generate-cover` ->（可选）首帧图
- 执行侧必须采用“`执行一步 -> 写状态 -> 读状态 -> 判定下一步`”循环，禁止批量并行后一次性回填状态

## 续跑判定循环（必须）

每一步后都执行以下检查：

1. 读取 `cut_koubo_state.json`
2. 若存在 `failed`：先返回失败步骤与修复建议，等待用户“继续/重试”后从该步骤恢复
3. 若存在 `running`：优先确认该步骤是否已落盘成功；成功则改 `completed`，失败则改 `failed`
4. 若存在 `pending`：继续执行最小序号的 `pending` 步骤
5. 若只剩 `completed|skipped`：再做一次 `query-draft` 总校验后才结束

判定口令（会话层）：
- 用户说“继续/继续执行/接着跑”时，必须触发上面的续跑循环，而不是重新生成全新计划
- 用户说“重剪”时，才允许新建一套状态文件重新开始

## 推荐调用方式

远程 URL（在会话中调用 cut-koubo）：

```bash
调用 cut-koubo，输入：
{
  "video_url": "https://example.com/koubo.mp4",
  "broll_urls": [
    "https://example.com/broll1.mp4",
    "https://example.com/broll2.mp4"
  ],
  "max_duration_seconds": 180
}
```

本地文件（先手动 `sts-upload`，再调用 cut-koubo）：

```bash
先调用 sts-upload 拿到公网 URL，再调用 cut-koubo，输入：
{
  "video_url": "https://uploaded.example.com/koubo.mp4",
  "broll_urls": ["https://uploaded.example.com/broll1.mp4"]
}
```

人物画中画分支：

```bash
调用 cut-koubo，输入：
{
  "video_url": "https://example.com/koubo.mp4",
  "use_human_pip": true
}
```

## 输出要求

- 成功时返回：
  - `draft_id`
  - `draft_url`
  - `state_file`（状态文件绝对路径）
  - 每一步执行状态与校验摘要
- 失败时返回：
  - `state_file`（状态文件绝对路径）
  - 失败步骤
  - 原始错误
  - 下一步修复建议（优先 `query-draft` + `vectcut-api-search` 检索 `modify*`）

## 后续建议

- 草稿生成后，如需导出可播放视频，提示用户调用 `cloud-render` 进行云渲染导出。
