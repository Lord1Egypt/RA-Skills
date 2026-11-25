## Description:

Validates and packages local skills, then submits them to SkillHub through a selected signed-in browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

Skill authors use this tool to validate and package a local skill, upload its archive and icon, and submit it to SkillHub through a specifically selected signed-in browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags possible packaging of files reached through symbolic links outside the skill directory; analysis is incomplete and does not establish that private files were disclosed.

Mitigation: Review symlink handling in the packaging behavior and ensure archive contents stay within the skill directory before publishing; avoid sensitive external symlink targets.

## Reference(s):

- [Easy WebBridge](https://github.com/xxjrq/easy-webbridge)
- [SkillHub publish page](https://skillhub.cn/dashboard/publish)
- [ClawHub skill page](https://clawhub.ai/xxjrq/skills/workbuddy-skillhub-publish)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [Skill ZIP archive and a concise publishing status report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports whether the release was submitted, is awaiting review, or needs user action.]

## Skill Version(s):

1.0.19 (source: release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
