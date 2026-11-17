## Description:

Helps agents select and run Qinghu AI workflows for ecommerce video creation, image editing, and short-video or creator data tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce creators and marketing teams use this skill to choose Qinghu workflows, estimate costs, submit authorized image or video jobs, and retrieve results or track creator data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad triggers may route unrelated requests into a paid Qinghu workflow.

Mitigation: Confirm the user's intent to use Qinghu before selecting or submitting a workflow.

Risk: Tool installation and token setup grant a third-party CLI access to credentials and media.

Mitigation: Confirm the package source and installation with the user; provide a Qinghu token only when the CLI is trusted, and review local media before upload.

Risk: Submitting a workflow may upload media and incur charges.

Mitigation: Review the estimate and obtain approval before uploading media or submitting a paid job.

Risk: Editing or repurposing third-party images and video may infringe rights.

Mitigation: Use only media owned by the user or for which the user has authorization.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-workflow-apps)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text, Media links]

**Output Format:** [Markdown with inline commands, job status, and result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports estimated credits before submission and actual credits after completion.]

## Skill Version(s):

0.1.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
