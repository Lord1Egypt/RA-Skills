# Six Thinking Hats Protocol

Use this protocol when `metadata.discussion_structure` is `six_hats`. It implements Edward de Bono's Six Thinking Hats method inside a roundtable-forge discussion.

## Core principle

In standard roundtable mode, each character speaks from their own domain. In six-hats mode, **all characters think from the same hat color at the same time**, then the group switches to the next hat together. This forces parallel thinking and prevents adversarial looping.

A character's domain expertise still flavors *how* they approach a hat, but the hat defines *what kind of thinking* is allowed in that phase.

## The six hats

| Hat | Color code | Thinking mode | Allowed content | Forbidden content |
|-----|-----------|---------------|-----------------|-------------------|
| White | `white` | Facts & data | Objective information, numbers, what is known, what is missing. | Opinions, emotions, judgments. |
| Red | `red` | Emotion & intuition | Feelings, hunches, gut reactions, fears, hopes. No justification needed. | Demands for evidence, logic chains. |
| Black | `black` | Caution & risk | Potential problems, failures, why it might not work, risks. | Optimism, benefits (save for yellow). |
| Yellow | `yellow` | Optimism & value | Benefits, value, feasibility, why it could work, opportunities. | Risks, downsides (save for black). |
| Green | `green` | Creativity & alternatives | New ideas, alternatives, provocations, "what if". | Critique of others' ideas during this phase. |
| Blue | `blue` | Process & control | Organizing the thinking, summarizing, meta-reflection, next steps. | Substantive domain content. |

Blue hat is worn by the **Conductor** (or Host in podcast mode). The other five hats are worn by all characters in parallel.

## Recommended hat sequence

The default sequence for a full six-hats pass on one focus question:

1. `blue_open` — Conductor frames the question and the process.
2. `white` — What do we know?
3. `red` — What do we feel about it?
4. `yellow` — What is the value here?
5. `black` — What are the risks?
6. `green` — What are the alternatives?
7. `blue_close` — Conductor synthesizes and decides next focus.

For a faster pass, use the **short sequence**: `blue_open → white → yellow → black → green → blue_close` (skip red).

For an emotionally charged topic, use the **empathy sequence**: `blue_open → red → white → yellow → black → green → blue_close` (start with feelings to surface tensions early).

## Conductor behavior

Under six-hats mode, the Conductor:

1. **Announces each hat switch** explicitly: "现在我们戴上白帽，只谈事实和数据。"
2. **Enforces the hat constraint**: if a character drifts into the wrong thinking mode, the Conductor redirects: "这部分留到黑帽阶段。"
3. **Dispatches all characters for each hat** before switching. Every character must contribute at least one speech per hat (or explicitly pass).
4. **Writes `structure_context.current_hat`** to Memory for every speech.
5. **May invite the user** at hat boundaries, especially after `red` (to check alignment) or after `black` (to decide whether to proceed).

## Character speaking constraints in six-hats mode

- **Stay in hat**: each speech must clearly belong to the current hat's thinking mode.
- **Short and focused**: 100–200 words per speech for non-blue hats (shorter than standard mode, because multiple characters speak per hat). **Blue hat** (Conductor only) allows **200–280 words** because opening framing and closing synthesis carry higher information density.
- **Label the hat implicitly**: start with the hat's mindset, e.g., white hat starts with "数据显示…", red hat starts with "我的直觉是…".
- **Domain flavor**: bring your expertise to bear on the hat, but do not switch hats.

### Example (white hat)

> **数据科学家李航**：截至 2026 年第二季度，全球使用 Agentic UI 的企业占比约为 18%。MCP 协议在开发者社区的采用率从 2025 年的 5% 上升到 22%。但"使用"和"有效使用"之间的差距，目前没有可靠数据。

### Example (red hat)

> **数据科学家李航**：我的直觉是，这些数据背后藏着一种"假装在用"的现象。人们填了表单、点了按钮，但并没有真正改变工作流。这让我有点不安。

## Per-hat focus questions

The Conductor should pose a clear focus question for each hat:

| Hat | Sample focus question |
|-----|----------------------|
| White | 关于这个议题，我们掌握哪些事实和数据？还有哪些信息是缺失的？ |
| Red | 直觉上你怎么看？你的第一反应是兴奋、恐惧还是困惑？ |
| Yellow | 如果这件事做成了，最大的价值是什么？谁受益？ |
| Black | 最可能失败的地方在哪里？有什么我们没看到的风险？ |
| Green | 有没有完全不同的做法？如果推倒重来，你会怎么设计？ |

## Output considerations

- Six-hats rounds tend to be **longer and more structured** than standard rounds. A full pass on one focus question typically produces 5–7 hat phases × 3–5 characters × 100–200 words (blue hat up to 280) = 1,500–7,500 words per question.
- This naturally solves the "podcast too short" problem: `six_hats + podcast` produces dense, multi-perspective content.
- The renderer (`render_memory_to_markdown.py` or `render_memory_to_podcast_script.py`) groups speeches by `structure_context.current_hat` and labels each phase.

## Interaction with other features

- **Fusion thinker**: the fusion thinker shines in `green` and `blue_close` phases, where synthesis and alternatives are most valued.
- **Temporal grounding**: `white` hat claims must be grounded in `metadata.current_date` and web-verified when claiming specific capabilities or adoption figures.
- **Conductor invitation**: best placed after `red` (emotional alignment check) or between `black` and `green` (decide whether to keep going).
- **Continuation**: `next_steps` from a six-hats pass are richer because they are tagged with the hat that surfaced them.
