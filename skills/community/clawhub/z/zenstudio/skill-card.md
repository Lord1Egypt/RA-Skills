## Description:

ZenStudio CLI helps agents use the ZenStudio platform through the zencli command line tool for AI image and video generation, project management, asset and material workflows, canvas operations, and file upload or download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoda](https://clawhub.ai/user/zhaoda)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to install and operate ZenStudio CLI for AI content creation workflows, including generation, media management, project work, and canvas updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a ZenStudio API key and can persist credentials in a local config file.

Mitigation: Use interactive login or protected secret handling, keep the config file private, and set ZENCLI_CONFIG_DIR deliberately in non-persistent or shared environments.

Risk: ZenStudio commands can write, delete, overwrite, upload, download, or call generic platform tools.

Mitigation: Confirm project, asset, material, canvas, and task identifiers before executing commands that change remote content.

Risk: The release notes and skill text state that ZenStudio CLI has migrated to WorkRally and future features will be published there.

Mitigation: Prefer the WorkRally package and skill for new workflows, and use this legacy skill only when the ZenStudio CLI integration is specifically needed.

## Reference(s):

- [ZenStudio skill page](https://clawhub.ai/zhaoda/skills/zenstudio)
- [Publisher profile](https://clawhub.ai/user/zhaoda)
- [ZenStudio homepage](https://ai.tvi.v.qq.com/zenstudio)
- [ZenStudio API key configuration](https://ai.tvi.v.qq.com/zenstudio/open-api)
- [WorkRally migration skill](https://clawhub.ai/tencent-adm/workrally)
- [WorkRally npm package](https://www.npmjs.com/package/workrally)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown, Code]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON-oriented CLI command guidance when the user needs agent-readable ZenStudio responses.]

## Skill Version(s):

1.3.7 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
