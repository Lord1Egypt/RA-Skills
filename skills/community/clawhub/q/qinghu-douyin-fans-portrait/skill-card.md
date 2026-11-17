## Description:

Retrieves Douyin creator audience profiles by account link, including age, gender, interests, devices, and geographic distribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Marketers and creator analysts use this skill to summarize the audience of a Douyin account from its profile or video link before planning campaigns or collaborations.

### Deployment Geography for Use:

China (Qinghu domestic service)

## Known Risks and Mitigations:

Risk: The skill may install or update npm tooling and make persistent local environment changes.

Mitigation: Review installation steps first; prefer a platform-managed, pinned qhkit installation.

Risk: The skill needs a Qinghu API token and may change local credential configuration.

Mitigation: Use a managed secret where possible and review token storage and site selection before use.

Risk: Audience queries are paid and actual charges may exceed the estimated base price.

Mitigation: Check the current estimate and obtain user consent before paid calls, particularly for bulk requests.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-douyin-fans-portrait)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Analysis]

**Output Format:** [Markdown audience summary with profile breakdowns and usage costs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the available Douyin audience data; label the source and applicable sample or period when provided.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
