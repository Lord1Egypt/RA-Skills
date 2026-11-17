## Description:

Searches Xiaohongshu by keyword with browser automation, manages login cookies, and sends retrieved note summaries to a Feishu group as card-style results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xie07418](https://clawhub.ai/user/xie07418)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this OpenClaw skill to trigger Xiaohongshu keyword searches from Feishu and receive a short set of note titles, links, authors, and engagement signals in the target group.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package ships sensitive Feishu credentials, hardcoded chat IDs, and a Xiaohongshu session cookie.

Mitigation: Rotate the exposed Feishu secret, revoke the bundled Xiaohongshu session, remove cookie.txt and hardcoded destination IDs from the release, and require deploy-time secrets configuration.

Risk: Search text can reach shell execution through the skill wrapper.

Mitigation: Replace shell string execution with argument-based process spawning and validate the keyword before invoking the Python crawler.

Risk: The skill can post search results or login QR screenshots to a configured Feishu destination.

Mitigation: Require an explicit, validated destination and restrict QR-code/login image posting to approved groups.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xie07418/skills/xhs-crawler-xie)
- [Artifact SKILL.md](artifact/SKILL.md)
- [Artifact usage documentation](artifact/使用文档.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Plain text status messages, Markdown-style help text, Feishu card messages, and JSON-like result objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default search output is limited to five Xiaohongshu notes and may include note titles, links, authors, like counts, and execution status.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
