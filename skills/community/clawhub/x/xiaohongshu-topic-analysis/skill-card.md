## Description:

当用户需要做小红书选题、xhs内容选题、rednote笔记选题策划、爆款角度拆解、内容方向规划或选题素材整理时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content operators, market researchers, brands, and creators use this skill to gather structured Xiaohongshu topic, note, comment, and creator activity data for content planning, competitive analysis, KOL screening, and audience insight work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send Xiaohongshu keywords or URLs to guaikei.com with the configured API token.

Mitigation: Use only intended public research targets, avoid sharing sensitive URL parameters, and rotate or revoke the token if it may have been exposed.

Risk: Successful fetched results and URL tokens may be automatically saved in a predictable temporary log folder.

Mitigation: Run on trusted machines, delete local logs after use, and prefer a version that redacts xsec_token values and makes saving opt-in.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/why20261/skills/xiaohongshu-topic-analysis)
- [Server-resolved Source Repository](https://github.com/why20261/xiaohongshu-topic-analysis)
- [Homepage](https://github.com/um-why/xiaohongshu-openclaw-skill)
- [Options Reference](references/options.md)
- [Troubleshooting Reference](references/troubleshooting.md)
- [Changelog](references/changelog.md)
- [Guaikei API Token Site](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and structured JSON command results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and GUAIKEI_API_TOKEN; command results may be saved locally by the skill.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
