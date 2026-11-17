## Description:

Retrieves a Douyin creator's posted videos from a profile URL, with cursor-based pagination through Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and analysts use this skill to retrieve a Douyin account's video list for recent-post reviews and competitor research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video-list requests incur Qinghu credits, especially when retrieving many pages.

Mitigation: Check the credit estimate and obtain user approval before paid calls; report actual credits charged.

Risk: Using the skill sends Douyin profile URLs to Qinghu and requires a Qinghu API token.

Mitigation: Confirm the user accepts the external service and provide the token only through the intended configuration or environment variable.

Risk: Setup may install or update qhkit and Node tooling on the user's machine.

Mitigation: Review and approve installation or updates before running them.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-douyin-creator-videos)
- [Qinghu qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise Markdown summary with video data; file for larger result sets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to 20 videos per page with cursor pagination; reports Qinghu credits spent on paid calls.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
