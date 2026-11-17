## Description:

技能商店客户端，支持查询在线技能、一键下载安装技能包

This skill is ready for commercial/non-commercial use.

## Publisher:

[pig-gua](https://clawhub.ai/user/pig-gua)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to list, search, inspect, download, and install skills from a trusted local skill-shop service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can write, overwrite, or delete local files based on untrusted server and archive data.

Mitigation: Use only with a trusted local skill-shop service and trusted packages; validate filenames, archive members, destination paths, and package integrity before installation.

Risk: The security verdict is suspicious.

Mitigation: Review the skill carefully before installing or running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pig-gua/skills/skill-shop)
- [Publisher profile](https://clawhub.ai/user/pig-gua)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Command-line text output with usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, unzip, and a trusted local skill-shop service.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
