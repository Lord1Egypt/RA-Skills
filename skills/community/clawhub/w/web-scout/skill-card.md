## Description:

Web Scout helps agents collect web and social platform content through Agent Reach integrations for websites, search, RSS, GitHub, video sites, and selected social platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aizain](https://clawhub.ai/user/aizain)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to equip an agent with web collection commands and setup guidance across search, web pages, feeds, repositories, videos, and social platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install mutable remote code and supporting tools.

Mitigation: Review before installing, use dry-run or safe mode first, install only the platforms needed, and prefer pinned commits, releases, or Docker digests where available.

Risk: Some platform integrations require live session cookies or logged-in accounts.

Mitigation: Avoid giving real account cookies unless the upstream tools and local environment are trusted; use throwaway accounts where possible.

## Reference(s):

- [ClawHub Web Scout release](https://clawhub.ai/aizain/skills/web-scout)
- [Agent Reach upstream project](https://github.com/Panniantong/Agent-Reach)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform-specific setup and credential-handling guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
