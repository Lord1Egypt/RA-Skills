## Description:

Manage torrents with qBittorrent through its WebUI API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmagar](https://clawhub.ai/user/jmagar)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and operators use this skill to list, add, pause, resume, delete, recheck, categorize, tag, and inspect torrents in qBittorrent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control important or private qBittorrent downloads.

Mitigation: Review the skill before installation and use it only with a qBittorrent WebUI instance you intend the agent to manage.

Risk: The skill reads qBittorrent WebUI credentials from a config file or environment variables.

Mitigation: Use restrictive permissions for the credential file, avoid shared machines, and prefer a local-only or HTTPS WebUI.

Risk: Delete commands can remove torrents and, with `--files`, downloaded content.

Mitigation: Require explicit user confirmation before executing delete operations, especially commands that include `--files`.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and qBittorrent API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include torrent metadata such as hash, name, state, progress, speed, ETA, category, tags, and save path.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
