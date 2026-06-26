# Interactive Routing Prompt

## Purpose

This mechanism lets the user confirm complexity, mode, and depth before the agent commits to a potentially costly or risky path.

## Trigger conditions

Use interactive routing when:

- the task is not explicit enough
- the user uses broad verbs such as `整理`, `优化`, `重构`, `分析`, `处理`
- the output form is unclear
- the task may touch files or folders
- the task may read a knowledge base
- the task may take multiple steps
- token cost may be meaningful
- the correct mode is uncertain

## Do not trigger when

The task is simple, clear, low-risk, and one-shot.

Principle:

`Simple, clear, low-risk tasks should not be slowed down by unnecessary confirmation.`

中文解释：

`简单、明确、低风险任务不要被不必要的确认流程拖慢。`

## The three routing questions

Ask at most:

1. complexity
2. mode
3. output depth

Do not ask ten follow-up questions at this stage.

If the real need is not yet calibrated, prefer a need-calibration prompt instead of stacking a second full routing prompt.

## Shortcut code system

### Complexity codes

- `S` = Simple
- `M` = Medium
- `C` = Complex

### Mode codes

- `A` = Ask Mode
- `P` = Plan Mode
- `C` = Craft Mode
- `E` = Expert Mode

### Depth codes

- `M` = Micro
- `S` = Standard
- `D` = Deep
- `F` = Artifact

Examples:

- `SPM`
- `MPS`
- `CCD`

## Risk conflict handling

If the user chooses an unsafe combination, do not follow it blindly.

Example warning:

`这个任务虽然你选择了 Craft Mode，但它涉及批量知识库整理，属于中高风险操作。为了避免误删、误改和 token 浪费，我需要先进入 Plan Mode，列出处理范围和执行步骤，等你确认后再执行。`

## Default recommendations

| Task situation | Suggested default |
|---|---|
| 简单明确低风险 | Craft + Standard |
| 报错诊断 | Ask + Standard |
| 模糊任务 | Ask + Micro or Plan + Standard |
| 文件修改 | Plan + Standard |
| 批量操作 | Plan + Standard |
| 知识库分析 | Plan + Standard |
| 长文写作 | Plan + Standard |
| 用户要求省 token | Ask or Craft + Micro |
| 多次失败 | Expert + Standard |

If the user does not want to choose, recommend:

`如果你不想选择，我建议使用：Plan Mode + Standard。`

## Channel-specific guidance

- WeChat, Yuanbao, iMA Copilot chat: use the minimal prompt
- WorkBuddy file tasks: use full routing plus file-safety confirmation
- iMA knowledge tasks: ask for retrieval scope before deep analysis
- iMA first-turn replies should also include a short understanding lock sentence and a one-screen answer target
- when the platform supports chips or quick replies, present the options in a button-ready format from `references/chat_confirmation_affordances.md`

## Session memory guidance

If the user already set a mode or depth preference earlier in the same session and the task type remains similar, reuse it instead of asking again.
