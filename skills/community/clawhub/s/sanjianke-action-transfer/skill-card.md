## Description:

Helps users submit and track action-transfer jobs that animate a reference person using the motion in an input video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Creators and developers use this skill to submit a reference image and input video to the a7w action-transfer service, then check the task and retrieve the resulting video URL. An a7w API key and publicly accessible media URLs are required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included client can list and call a7w apps beyond action transfer, potentially exposing available apps or spending account points.

Mitigation: Review the client before installation, use a limited API key if available, and restrict calls to the intended action-transfer endpoints.

Risk: Changing the API host could send the API key to an untrusted endpoint.

Mitigation: Do not set --host or A7W_HOST unless you fully trust the endpoint.

Risk: Uploading face or video media can expose private or non-consensual material.

Mitigation: Use only media you have permission to share; avoid private or non-consensual face and video material.

Risk: Submitting a task can consume account points, and repeat submissions may incur additional charges.

Mitigation: Check the expected cost and task status before retrying a submission.

## Reference(s):

- [Action-transfer submission API](references/api-submit.md)
- [Action-transfer task query API](references/api-query.md)
- [Getting started and API key setup](references/getting-started.md)
- [a7w API and account portal](https://api.a7w.cn/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON task status and video URL]

**Output Format:** [Markdown guidance and shell commands; JSON responses from the service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated MP4 is hosted by the service; the client returns its URL when the task completes.]

## Skill Version(s):

1.0.6 (source: ClawHub release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
