# Template: paper-interpretation

用于将论文或论文相关资料转换为小红书“论文解读”博文。

## Humanization Hint

- 若环境中存在 `humanizer-zh` skill，可在最终定稿前做一轮“口语化和人味润色”。
- 不要求强依赖该 skill；不可因润色改变事实含义与数据结论。

## Parameters

- `length`: `short` / `medium` / `long`
- `emoji_density`: `low` / `medium` / `high`

默认:

- `length=medium`
- `emoji_density=medium`

## Title Strategy (High-Attraction)

目标: 标题更吸引人、更有冲突感和悬念感，但不编造事实。

生成要求:

1. 必须先给 5 个候选标题，再选 1 个 `final_title`。
2. 每个标题控制在 16-24 字，优先短句+停顿。
3. 至少包含以下元素中的 2 项:
   - 明确收益（如“性能翻倍”“读懂就能用”）
   - 冲突/反常识（如“不是更大模型才更强”）
   - 数字锚点（如“3 个结论”“1 张图看懂”）
   - 行动导向（如“建议先看第 4 部分”）
4. 允许“唬人感”表达，但不得使用无法从原文验证的夸张结论。

标题公式示例（按论文内容替换）:

- `我以为这方向凉了，结果这篇直接把 {指标/任务} 打穿`
- `别再盲目刷论文了：这篇只讲 3 件真有用的事`
- `看完这篇我改了实验方案：{方法名} 真正强在这里`
- `这篇不是小修小补，它把 {任务} 的底层逻辑改了`
- `{年份/会议} 最该先读的一篇？先看它的第 4 个实验`

## Output Markdown Skeleton

```markdown
# {final_title}

## 📌 论文名称：《{paper_title}》

## {emoji?} 1) 这篇论文在解决什么问题
{研究问题与动机，1-2 段}

## {emoji?} 2) 作者的核心思路是什么
{方法主线，1-2 段}

## {emoji?} 3) 方法亮点拆解
- {亮点1}
- {亮点2}
- {亮点3}

## {emoji?} 4) 实验结果怎么看
{关键结果 + 指标/对比；缺失则说明原文未明确给出}

## {emoji?} 5) 局限性与风险
{至少 1 条，优先作者原文}

## {emoji?} 6) 一句话总结
{一句价值总结}

## {emoji?} 7) 你怎么看？
{互动问题，引导评论}

#标签1 #标签2 #标签3 #标签4 #标签5
```

论文名称输出要求:

- 在正文第一个小标题固定输出：`## 📌 论文名称：《{paper_title}》`。
- `paper_title` 优先使用论文原始标题；无法确定时写：`《原文未明确给出》`。
- 不得擅自翻译或改写标题语义；如需翻译，附在后文说明中而非替换原题。

标题输出附加要求:

- 在正文最前面单独列出：
  - `标题候选：`
  - `1. ...`
  - `2. ...`
  - `3. ...`
  - `4. ...`
  - `5. ...`
- 再给出 `最终标题：{final_title}`，然后进入正文。

## JSON Shape

```json
{
  "post_type": "paper-interpretation",
  "title_candidates": ["..."],
  "final_title": "...",
  "body_sections": [
    {"name": "research_problem", "content": "..."},
    {"name": "core_idea", "content": "..."},
    {"name": "method_highlights", "content": ["...", "..."]},
    {"name": "results", "content": "..."},
    {"name": "limitations", "content": "..."},
    {"name": "one_line_summary", "content": "..."},
    {"name": "engagement_question", "content": "..."}
  ],
  "emoji_density_level": "medium",
  "hashtags": ["#..."],
  "evidence_notes": [
    {"section": "research_problem", "source": "..."},
    {"section": "results", "source": "..."}
  ]
}
```

## Reliability Requirements

1. 数值、对比、结论必须可在输入中定位。
2. 若无明确证据，写“原文未明确给出”。
3. 不得把猜测写成事实。
4. 互动问题应围绕论文真实争议点，不制造伪争议。
5. 标题可以强吸引，但不能超出论文真实结论边界。

## Length Guidance

- `short`: 300-500 中文字
- `medium`: 500-900 中文字
- `long`: 900-1400 中文字

## Emoji Guidance

- Emoji 放置优先级：`小标题 > 标题行 > 正文`。
- 正文默认不加 Emoji；仅在用户明确要求时，且单段最多 1 个。
- `low`: 给 2-3 个关键小标题加 Emoji。
- `medium`: 给 4-6 个小标题加 Emoji。
- `high`: 给 7-8 个小标题加 Emoji，正文仍尽量不加。

## Hashtag Guidance (Domain-first)

- 最终 `hashtags` 优先使用中文或英文专业术语（如任务名、方法名、数据集名、评测指标、应用领域）。
- 避免使用泛流量词、情绪词、口语化标签（如“太强了”“必看”）。
- 建议结构：`主题术语` + `方法/模型术语` + `场景/行业术语` + `人群术语`。
- 生成 `hashtags` 前先判断文章所属研究领域（如 NLP/CV/推荐系统/医疗 AI 等），并据此优先选择该领域高相关术语标签。
- 若原文信息不足，标签可保守化并在 `evidence_notes` 说明依据与不确定性。
