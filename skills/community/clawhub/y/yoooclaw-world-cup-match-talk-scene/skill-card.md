## Description:

Generates Chinese World Cup football match talking-point packs for chats, watch parties, commentary prep, and social posts, with optional use of recent phone notifications when the user requests notification or fan-group context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to prepare concise, reusable World Cup football talking points for group chats, offline match watching, commentary notes, and social media posts. When requested, it can summarize relevant recent phone notifications into fan-group context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read broad recent phone notifications if notification or fan-group context is requested without a narrow app, group, or time range.

Mitigation: Use the skill only with a confirmed narrow notification scope, extract only match-relevant signals, and avoid exposing unrelated notification content.

Risk: The bundled public-source probing script weakens HTTPS verification and source allowlisting, which can reduce trust in fetched public-source material.

Mitigation: Treat script results as diagnostic support, cross-check key facts through public search or trusted sources, and mark partial, blocked, inferred, or unverified information clearly.

Risk: Generated match commentary can blend reported facts, public opinion, and tactical inference.

Mitigation: Separate facts, opinion, inference, and unverified claims in the output, especially for match times, scores, standings, injuries, lineups, records, and official statements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/skills/yoooclaw-world-cup-match-talk-scene)
- [30-second match template](artifact/references/template-30s.md)
- [Main talking points template](artifact/references/template-main-points.md)
- [Discussion topics template](artifact/references/template-discussion.md)
- [Talk lines template](artifact/references/template-talk-lines.md)
- [Social post template](artifact/references/template-social-post.md)
- [Chinese football source probing script](artifact/scripts/probe_cn_football_sources.py)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown prose with optional shell command snippets and structured talking-point sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are usually Chinese and may include uncertainty labels for public-source facts, opinion, inference, and unverified claims.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
