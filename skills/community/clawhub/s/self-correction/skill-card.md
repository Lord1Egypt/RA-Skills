## Description:

Self-Correction helps an agent detect Chinese user disagreement or correction cues and re-analyze the user's original intent before producing a revised answer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hauxu](https://clawhub.ai/user/hauxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill to improve conversational recovery when a Chinese-speaking user rejects, corrects, or clarifies a prior response. The skill guides the agent to revisit the original request, identify likely misunderstanding points, and answer from a corrected interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Chinese disagreement or follow-up phrases may trigger self-correction when the user only intended to add context.

Mitigation: When the corrected intent is ambiguous, ask a concise confirmation question before replacing the answer direction.

Risk: The bundled packaging validator is a convenience check and is not a comprehensive security review for future package contents.

Mitigation: Review and scan each release before deployment, especially if scripts or packaged files change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hauxu/skills/self-correction)
- [Publisher profile](https://clawhub.ai/user/hauxu)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown-style conversational response with optional code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a structured self-check, re-understood requirements, issue analysis, and revised answer when triggered.]

## Skill Version(s):

1.0.0 (source: server release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
