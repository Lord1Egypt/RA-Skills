# Example Visual Candidate Board Round - v1.0.1

This example occurs after a generated specialized skill has presented 4-6 text candidates. The next step is not final prompt generation; it is candidate-board setup.

## P4 TEXT_ONLY Candidate-Board Setup

### 当前执行计划

- 当前处于 P4：视觉候选图板设置（TEXT_ONLY）
- 上一步 P3 已给出 6 个文字候选方案
- 本步目标：设置 6 张候选图/示意图的生成规则

### 默认推荐

生成 6 张候选图。固定论文 thesis、核心模块和标签，只变化布局骨架，这样用户可以看图选方向，而不是只靠文字定稿。

### Candidate-board brief

- board type: layout / scheme
- candidate count: 6
- varied axis: layout skeleton
- fixed elements: figure thesis, required modules, exact labels, palette semantics
- rendering route: ChatGPT web Create image / ChatGPT Images 2.0; Codex `$imagegen` first; fallback ChatGPT Images 2.0 API or approved image API
- compare: reading clarity, contribution prominence, label readability, paper-slot fit

### 当前状态与产物

- **阶段：**Figure Production
- **当前步骤：**P4
- **当前回复模式：**TEXT_ONLY
- **全部步骤与当前位置：**P1(TEXT_ONLY) -> P2(TEXT_ONLY) -> P3(TEXT_ONLY) -> P4(TEXT_ONLY candidate-board setup) [当前位置] -> P5(IMAGE_ONLY candidate-board generation) -> P6(TEXT_ONLY candidate review/selection) -> P7(TEXT_ONLY final image brief) -> P8(IMAGE_ONLY formal generation) -> P9(TEXT_ONLY review/final text)
- **text_candidate_count：**6
- **image_candidate_count：**6
- **visual_candidate_board_status：**setup_ready
- **candidate_image_batch_id：**not_created
- **本轮新增产物：**candidate-board brief
- **待产物：**P5 IMAGE_ONLY candidate image board

## 下一步你可以这样问

1. `请使用**<当前skill名称>**，执行，根据当前状态，下一步执行：生成 6 张候选图/示意图供我比较选择。`
2. `请使用**<当前skill名称>**，根据当前状态，提供下一步提问建议。`

## P5 IMAGE_ONLY Candidate Board

P5 must contain only image generation/display. No prose, no state footer, no captions.

## P6 TEXT_ONLY Candidate Review

The next text turn after P5 must record the image batch, compare candidates, recommend one, and ask the user to select, revise, combine, or request another board.
