## Description:

Guides an agent in assessing suspected head-and-shoulders, double or triple top and bottom, rounding, and V-shaped chart patterns by checking prior trend, neckline or key-level breakout, and volume confirmation before treating them as reversals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bianchunhui](https://clawhub.ai/user/bianchunhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze possible technical-analysis reversal patterns, distinguish completed reversals from lookalike formations, and produce disciplined pattern-recognition guidance. It is useful when a chart discussion involves neckline breaks, target estimates, or deciding whether a suspected reversal is still only a watch condition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Technical-analysis pattern guidance may be mistaken for guaranteed trading advice.

Mitigation: Present outputs as probabilistic chart-analysis guidance and require independent review before making trading or risk decisions.

Risk: A merely similar chart shape can be overclassified as a completed reversal.

Mitigation: Require the documented completion checks: an existing prior trend, effective neckline or key-level breakout, and preferably volume confirmation.

Risk: Language-specific source material may be less clear to non-Chinese users.

Mitigation: Use clear language-neutral summaries when presenting the guidance to broader audiences.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/bianchunhui/murphy-ta-skills/tree/main/reversal-patterns)
- [ClawHub skill page](https://clawhub.ai/bianchunhui/skills/reversal-patterns)
- [Artifact skill definition](artifact/SKILL.md)
- [Artifact test prompts](artifact/test-prompts.json)

## Skill Output:

**Output Type(s):** [guidance, text, markdown]

**Output Format:** [Markdown prose with concise analytical guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, file writes, network access, or persistent state are produced by the skill.]

## Skill Version(s):

0.1.0 (source: release evidence and artifact test-prompts.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
