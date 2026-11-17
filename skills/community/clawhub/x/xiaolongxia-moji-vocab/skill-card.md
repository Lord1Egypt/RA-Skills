## Description:

Moji辞書生词本管理与每日测试技能。支持读取日语收藏夹、按时间排序（早期单词优先）、混合模式出题（释义+读音）、删除已掌握单词。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dadaniya99](https://clawhub.ai/user/dadaniya99)

### License/Terms of Use:

MIT

## Use Case:

External learners and developers use this skill to manage Moji Dictionary Japanese vocabulary favorites, review older saved words, generate daily quiz prompts, and remove words they have mastered.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live Moji session credentials and device identifiers.

Mitigation: Treat MOJI_TOKEN and MOJI_DEVICE_ID as secrets, prefer environment variables, and avoid sharing logs or screenshots containing credential values.

Risk: The skill can delete persistent Moji favorites from a user's account.

Mitigation: Use dry-run mode first and perform deletion actions only after confirming the exact words or levels to remove.

Risk: Security review classified the release as suspicious due to credential handling, deletion authority, and documentation accuracy concerns.

Mitigation: Review the behavior and configuration before installation, and verify documented commands against the files included in the release.

## Reference(s):

- [Moji Vocab on ClawHub](https://clawhub.ai/dadaniya99/skills/xiaolongxia-moji-vocab)
- [Moji Dictionary](https://www.mojidict.com)
- [Moji Dictionary API Endpoint](https://api.mojidict.com)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown and terminal text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Moji session credentials supplied by environment variables or command-line flags.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
