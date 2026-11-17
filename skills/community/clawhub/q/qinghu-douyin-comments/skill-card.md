## Description:

Collects comments from a Douyin video URL and summarizes audience feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

People researching audience feedback use this skill to collect and review comments on a specified Douyin video, with user approval before paid collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or update Node and qhkit on the user's machine.

Mitigation: Obtain explicit approval before installing or upgrading tools.

Risk: Setup can change local qhkit credentials and site configuration.

Mitigation: Confirm token and configuration changes with the user before applying them.

Risk: Comment-collection requests can incur variable charges, especially across multiple pages.

Mitigation: Estimate charges and obtain explicit approval for each paid collection batch.

Risk: Broad requests about feedback could trigger collection when no Douyin video is intended.

Mitigation: Use only for requests clearly identifying Douyin video comments or providing a Douyin video URL.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-douyin-comments)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files]

**Output Format:** [Concise text or Markdown summary; table file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Comments are retrieved in pages of 10; paid usage is reported in Qinghu credits.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
