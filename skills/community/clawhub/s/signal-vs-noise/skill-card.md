## Description:

Filter relevant information from noise; extract claims, dedupe, rank impact, and preserve evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzfshark](https://clawhub.ai/user/mzfshark)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to reduce a noisy dataset of messages, news, metrics, or notes into ranked decision-relevant signals with evidence and a brief noise bucket.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may activate the skill for general summarization requests.

Mitigation: Confirm that the user wants signal filtering, deduplication, and impact ranking before applying the skill to broad summarization tasks.

Risk: The skill may over-rank novel or urgent-looking items when evidence is weak.

Mitigation: Preserve evidence pointers, rank by impact and credibility, and label dissenting or weakly supported claims as low-confidence rather than deleting them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzfshark/skills/signal-vs-noise)
- [Publisher profile](https://clawhub.ai/user/mzfshark)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured text with ranked_signals and discarded_noise sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each ranked signal should include a claim, why it matters, and at least one evidence pointer.]

## Skill Version(s):

2.0.0 (source: skill.yml, SKILL.md metadata, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
