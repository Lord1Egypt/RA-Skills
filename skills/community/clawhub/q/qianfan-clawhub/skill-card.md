## Description:

Search and install Baidu Qianfan ecosystem skills with fuzzy matching across slug, name, and description fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baiduqianfangroup](https://clawhub.ai/user/baiduqianfangroup)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search Baidu Qianfan ecosystem skills and install selected skills by exact slug into a Qianfan workspace or custom skills directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can write files from downloaded skill archives into the selected skills directory.

Mitigation: Review the selected slug and target directory before installing, use an isolated work directory for testing, and avoid force overwrite unless the existing contents have been checked.

Risk: The Baidu API key can be sent to a caller-chosen endpoint when a custom endpoint is supplied.

Mitigation: Use the official Baidu endpoint and a low-privilege disposable BAIDU_API_KEY when testing or reviewing the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baiduqianfangroup/skills/qianfan-clawhub)
- [Publisher profile](https://clawhub.ai/user/baiduqianfangroup)
- [Baidu AppBuilder endpoint](https://appbuilder.baidu.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; search results list skill slugs and names, while install operations write downloaded skill files into the selected skills directory.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
