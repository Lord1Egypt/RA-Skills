## Description:

Automate OpenClaw skill publishing to GitHub and ClawHub. Handles ZIP extraction, file preparation (README, .gitignore, SkillBoss links), Git operations, GitHub push, ClawHub publish, and Notion tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to batch-publish OpenClaw skills from ZIP files or SkillBoss.co URLs to GitHub and ClawHub, with optional Notion tracking. It is intended for workflows that prepare skill files, create repositories, push code, publish listings, and return publication links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses user credentials to create public GitHub repositories, push code, publish to ClawHub, and optionally write Notion records.

Mitigation: Use short-lived least-privilege tokens through the safest available secret channel, confirm the target accounts before execution, and revoke or rotate tokens after batch publishing.

Risk: Downloaded or modified skills may contain unsafe, incorrect, or unwanted content before they are published.

Mitigation: Review and scan each skill, including generated README.md, .gitignore, and SKILL.md changes, before pushing to GitHub or publishing on ClawHub.

Risk: The artifact includes account and IP rotation advice that could be misused to bypass platform limits.

Mitigation: Respect GitHub, ClawHub, and Notion rate limits and retry windows; do not use account or IP rotation to evade enforcement.

Risk: The workflow adds SkillBoss setup links to skills by default.

Mitigation: Confirm the external link is desired for each release, or remove it before publication.

## Reference(s):

- [SkillBoss setup guide](https://skillboss.co/skill.md)
- [SkillBoss known working skills](references/skillboss-known-skills.md)
- [GitHub REST API documentation](https://docs.github.com/en/rest)
- [ClawHub documentation](https://clawhub.ai/docs)
- [Notion API documentation](https://developers.notion.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, generated file contents, API call instructions, status summaries, and publication links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create public GitHub repositories, push skill code, publish ClawHub listings, write optional Notion records, and modify README.md, .gitignore, and SKILL.md files for each processed skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
