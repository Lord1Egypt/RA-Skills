## Description:

Helps agents submit up to 20 Douyin, Xiaohongshu, or Bilibili video links for engagement statistics and deliver the resulting Excel spreadsheet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Content and marketing teams use this skill to collect video engagement metrics for their own or authorized short-form videos, compare performance, and export results to Excel. It uses Qinghu's paid workflow and requires a Qinghu token.

### Deployment Geography for Use:

Global (uses Qinghu's China-region service)

## Known Risks and Mitigations:

Risk: Provided video links are sent to Qinghu's service.

Mitigation: Submit only links you are comfortable sharing with Qinghu, and use only owned or authorized content.

Risk: The workflow requires a Qinghu token and may consume paid credits.

Mitigation: Handle the token securely, check the live estimate, and obtain confirmation before submitting a paid job.

Risk: Installing or upgrading the qhkit package introduces a software supply-chain dependency.

Mitigation: Review or pin the package version where your environment requires strict supply-chain control.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shortvideo-data-engine)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with an Excel (.xlsx) download link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single submission of up to 20 full video links; the skill returns the workflow's completed spreadsheet without interpreting its data.]

## Skill Version(s):

0.1.6 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
