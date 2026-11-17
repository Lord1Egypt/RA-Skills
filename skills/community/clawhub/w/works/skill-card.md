## Description:

Personal project intelligence for keeping multi-session efforts in per-project folders with status, next steps, progress logs, and wiki links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilyabelikin](https://clawhub.ai/user/ilyabelikin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Works to maintain private local records for ongoing projects that span sessions, including current status, dated progress, next steps, related artifacts, and links to connected personal knowledge files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically create and modify private project records and related personal knowledge files.

Mitigation: Review proposed file paths and content before first-time setup, new project creation, cross-link writes, or closing and moving project folders.

Risk: Mutable remote install or update paths can replace the local skill file with changed upstream content.

Mitigation: Use pinned, reviewed installation and update steps, and scan updates before replacing the installed skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ilyabelikin/skills/works)
- [Skill definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [Digs companion skill](https://github.com/haah-ing/digs-skill)
- [Peeps companion skill](https://github.com/haah-ing/peeps-skill)
- [Nooks companion skill](https://github.com/haah-ing/nooks-skill)
- [Pages companion skill](https://github.com/haah-ing/pages-skill)
- [Vibes companion skill](https://github.com/haah-ing/vibes-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown project records, local file updates, shell commands, and concise text confirmations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local project files under mind/works/.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
