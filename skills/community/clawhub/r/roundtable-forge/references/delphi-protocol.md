# Delphi Method Protocol

Use this protocol when `metadata.discussion_structure` is `delphi`. It implements the Delphi method — anonymous multi-round convergence — inside a roundtable-forge discussion.

## Core principle

In standard mode, characters speak openly from their domain, which means seniority, charisma, or domain authority can suppress minority views. In Delphi mode, **speaker identity is hidden across all rounds**: every contribution is attributed only to an anonymous label (`专家 #1`, `专家 #2`, …). This forces the group to evaluate arguments on their merits, not on who said them.

The method proceeds in multiple rounds. Each round narrows the dispersion of opinions until the group reaches either consensus or a clearly articulated divergence.

## The three phases

A full Delphi pass on one focus question uses two to three rounds, each mapped to one Memory `round`:

| Phase | `delphi_phase` | What happens | Conductor role |
|-------|---------------|--------------|----------------|
| Independent | `independent` | Every character answers the focus question independently, without seeing others' responses. | Distribute the question, collect answers, do not evaluate. |
| Feedback | `feedback` | The Conductor distributes an anonymized summary of all Round-1 answers. Each character revises, defends, or shifts their position after reading peers' arguments. | Compile the anonymous digest, highlight where answers cluster and where they diverge, invite revision. |
| Convergence | `convergence` | The Conductor extracts the consensus points and the remaining disagreements. Characters confirm or register a final dissent. | Synthesize, label each point as `consensus` / `divergence` / `open`, close the pass. |

For a fast pass, skip `convergence` and stop after `feedback` (two rounds total).

For a deep pass on a highly sensitive topic, insert an extra `feedback` round before `convergence` (three rounds total plus convergence = up to four).

## Anonymization mechanism

- **Memory retains `character_id`** for internal traceability, but **never displays the real name or role** during the discussion.
- Each speech carries `structure_context.anonymous_label` (e.g., `专家 #1`). The Conductor assigns labels in Round 1 and **keeps them stable** across rounds so the group can track how an individual's position evolved.
- The Conductor's digest in the `feedback` phase must paraphrase rather than quote verbatim if paraphrasing reduces the risk of identity leakage (e.g., dropping a phrase like "作为 CEO" that a character might slip in).

### Runtime enforcement

- **`single_backend_multi_session`**: anonymization is a rendering concern. The Conductor simply renders speeches with `anonymous_label` instead of the real name.
- **`real_subagent_runtime`**: the Conductor must strip identity from the context it sends to each subagent during the `feedback` phase. Each subagent sees only the anonymized digest, never the raw names of peers.

## Conductor behavior

Under Delphi mode, the Conductor:

1. **Opens with the question and the rules**: "接下来我们用德尔菲方法讨论这个问题。所有人独立作答，发言将以匿名方式展示。请聚焦论点本身。"
2. **Collects Round-1 answers silently** — does not comment, rank, or react until all are in.
3. **Produces the anonymous digest** for Round 2: groups similar positions, highlights divergences, quotes anonymously.
4. **Invites revision explicitly**: "看完其他专家的匿名观点后，你是否要修正或坚持自己的立场？"
5. **Closes with a labeled synthesis**: each key point tagged `consensus` / `divergence` / `open`.
6. **May invite the user** between phases, especially after `feedback` (to check if the convergence direction aligns with the user's intent).

## Character speaking constraints in Delphi mode

- **No identity leakage**: never reveal your role, title, or background. Do not say "作为技术负责人我认为…" or "在我们公司我们就是这么做的". Argue from the substance.
- **Engage with arguments, not people**: when referencing another participant's point, use the anonymous label: "专家 #3 提到的风险我认为可以进一步分解为…"
- **Length**: 150–300 words per speech. Shorter than standard mode because the value is in the iteration across rounds, not in any single monologue.
- **Evolution is expected**: changing your mind between Round 1 and Round 2 is a feature, not a weakness. Explicitly note what shifted and why: "我之前认为 X，但看到专家 #2 关于 Y 的论证后，我修正为…"
- **Dissent is valued**: if you disagree with the emerging consensus, say so clearly in the `convergence` round rather than quietly conforming.

### Example (independent phase)

> **专家 #1**：这个方案的核心假设是用户愿意为隐私付费，但现有市场数据并不支持这一点。即使是号称注重隐私的产品，其用户留存也主要靠功能而非隐私承诺。我认为风险被低估了。

### Example (feedback phase)

> **专家 #3**：专家 #1 对付费意愿的质疑让我重新思考。我原来从技术可行性角度判断方案可行，但如果用户根本不愿为这个能力掏钱，技术再成熟也没有商业意义。我修正我的立场：技术可行但不等于商业可行，需要先验证付费意愿。

## Per-phase focus questions

| Phase | Sample focus question |
|-------|----------------------|
| Independent | 对这个问题，你的独立判断是什么？给出你的核心结论和主要理由。 |
| Feedback | 看完其他专家的匿名观点后，你要修正、坚持还是调整你的立场？哪些观点改变了你的想法？ |
| Convergence | 基于两轮讨论，你认为哪些点是共识，哪些点仍有分歧？你对最终方案的态度是什么？ |

## Memory representation

Each Delphi round records the phase and anonymization metadata:

```json
{
  "round_number": 1,
  "discussion_structure": "delphi",
  "focus_question": "是否应该采用 X 方案？",
  "structure_context": {
    "delphi_phase": "independent",
    "anonymized": true,
    "participant_count": 4
  },
  "speeches": [
    {
      "character_id": "analyst_a",
      "content": "...",
      "structure_context": {
        "anonymous_label": "专家 #1"
      }
    }
  ]
}
```

The `convergence` round's `synthesis` section should tag each key point:

```json
{
  "round_number": 3,
  "discussion_structure": "delphi",
  "structure_context": { "delphi_phase": "convergence" },
  "synthesis": {
    "consensus": ["技术可行性得到认可"],
    "divergence": ["商业模式的付费意愿假设未验证"],
    "open_questions": ["是否需要先做 MVP 验证？"]
  }
}
```

## Output considerations

- Delphi rounds are **shorter per-speech** (150–300 words) but the multi-round structure produces comparable total volume to a standard round.
- The renderer (`render_memory_to_markdown.py` or `render_memory_to_podcast_script.py`) replaces the character name with `anonymous_label` and groups speeches by `delphi_phase`.
- In podcast mode, the Host introduces each phase: "第一轮，各位专家独立作答，身份匿名。" The Host remains identified — only the guests are anonymized.

## Interaction with other features

- **Temporal grounding**: factual claims must still be grounded in `metadata.current_date`, even under anonymity.
- **Conductor invitation**: best placed between `feedback` and `convergence` — the user can steer which divergence to prioritize.
- **Continuation**: `next_steps` from a Delphi pass should note which phase surfaced them and whether they represent consensus or divergence.
- **Character selection**: Delphi benefits from a **diverse** panel (different domains, different risk appetites) — homogeneity defeats the purpose of anonymity.
