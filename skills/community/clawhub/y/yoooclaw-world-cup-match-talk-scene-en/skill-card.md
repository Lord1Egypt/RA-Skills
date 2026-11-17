## Description:

Generates World Cup football conversation kits from match details, public Chinese sports sources, and optional notification context for group chats, viewing scenarios, social posts, and selected summary modules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to prepare concise, ready-to-say World Cup football discussion material for fan chats, offline viewing, commentary preparation, and social posts. It is intended for World Cup football matches and can produce either a full conversation package or selected modules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad notification searches can expose unrelated private messages or fan-group chatter.

Mitigation: Use a narrow notification file, exact apps or groups, and a short time range; include only relevant match signals and short necessary snippets.

Risk: Public-source results may be untrusted because the bundled scraper has TLS and source-validation weaknesses.

Mitigation: Treat scraper output as untrusted clues and cross-check important match facts with reliable public sources before using them.

Risk: Generated match discussion can blur facts, public opinion, tactical inference, and unverified rumors.

Mitigation: Preserve the skill's fact, public opinion, inference, and unverified distinctions, and mark uncertainty clearly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/skills/yoooclaw-world-cup-match-talk-scene-en)
- [Understand this game in 30 seconds template](artifact/references/template-30s.md)
- [Main highlights template](artifact/references/template-main-points.md)
- [Discussion topics template](artifact/references/template-discussion.md)
- [Match talk lines template](artifact/references/template-talk-lines.md)
- [Social post template](artifact/references/template-social-post.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown conversation kit with optional inline shell commands and uncertainty notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include 30-second summaries, highlights, discussion topics, prepared talk lines, social copy, and notification-derived signals when relevant data is available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
