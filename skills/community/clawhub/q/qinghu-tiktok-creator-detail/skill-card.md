## Description:

Looks up TikTok creator details for up to 10 user IDs or @usernames per request using Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and commerce teams use this skill to retrieve TikTok creator details by user ID or username, including available audience and commerce metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creator identifiers are sent to Qinghu for paid lookups, and charges may grow with the number of results.

Mitigation: Disclose the estimated credits and data recipient, obtain approval before paid calls, and report the actual credits charged.

Risk: The skill may install or update qhkit and Node on the host and store service credentials locally.

Mitigation: Review the tool before installing, prefer a preinstalled pinned qhkit version, and supply an ephemeral token through a secret manager.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-tiktok-creator-detail)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API key management](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise written summary; table file for 10 or more records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes supporting metrics and the credits charged for paid calls.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
