## Description:

Retrieves Douyin hashtag details by topic ID, including view counts and participation data, through Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to check the popularity and participation of a Douyin hashtag using its topic ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may install Node and npm tooling or change local configuration.

Mitigation: Review installation steps, prefer a preinstalled pinned qhkit version, and confirm before changing site or token configuration.

Risk: The skill requires a Qinghu API token and can spend Qinghu credits on lookups.

Mitigation: Handle the token securely, check the current estimate, and obtain user approval before paid calls or large batches.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-douyin-hashtag)
- [Qinghu qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown summary; tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports Qinghu credits spent on paid calls.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
