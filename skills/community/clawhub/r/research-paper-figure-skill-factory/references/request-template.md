# Request Template

Use this when turning a user request into a figure production brief.

## Minimal request

```text
请使用**<当前skill名称>**，执行，根据当前状态，下一步执行：帮我为这篇论文设计一张[图类型/位置]图。
论文材料：[粘贴摘要、方法、初稿或说明]
目标位置：[intro / method / results / appendix / rebuttal / slides]
偏好：[可选：3D / 卡通 / 磁贴 / 扁平 / 架构图 / 不确定]
参考图：[可选：上传1-3张]
```

## Full brief fields

- Paper title/topic:
- Core claim:
- Main problem gap:
- Contribution:
- Target figure slot:
- Desired figure category:
- Must include:
- Must avoid:
- Audience / reviewer sensitivity:
- Existing figures:
- Reference figures:
- Visual style preferences:
- Output needed now: plan / schemes / prompt / images / critique / caption

## If user is unsure

When the user does not know what to ask, tell them to use:

`请使用**<当前skill名称>**，根据当前状态，提供下一步提问建议。`

Normal follow-up turns should continue from the active session/history, so the user does not need to manually upload or paste state. Ask for the latest `当前状态与产物` only if history is unavailable, truncated, or moved to a new conversation.

## v1.0.0 multi-candidate request examples

Generated figure-making skills should include user-facing next-step examples such as:

- 请先给我 6 个候选文字方案。
- 请基于这 6 个候选文字方案，用 imagegen/API 生成 6 张候选图。
- 先不要只定一个方向，用 imagegen/API 给我看 4 张候选方案图。
- 请分别把方案 A / B / C 各用 imagegen/API 生成 1 张图给我比较；可以输出 PNG/JPEG/WebP 等原生位图结果，不要用 SVG、Mermaid 或代码绘图替代。
- 请基于同一个方案，生成 6 张不同布局风格的 imagegen/API 候选图。

