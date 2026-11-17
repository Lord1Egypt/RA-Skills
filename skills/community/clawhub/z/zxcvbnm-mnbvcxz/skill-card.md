## Description:

Executes AIVideoMaker API workflows for text-to-video and image-to-video generation, including task creation, status polling, task details retrieval, and cancellation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rainlin10](https://clawhub.ai/user/rainlin10)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to submit AIVideoMaker text-to-video or image-to-video jobs, poll generation status, retrieve task details, and cancel submitted tasks through a Node.js workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts, image inputs, and generated task requests to AIVideoMaker using the configured API key.

Mitigation: Avoid submitting sensitive, private, or proprietary prompts or images unless upstream processing and retention are acceptable.

Risk: AIVideoMaker usage may consume account credits, especially for longer videos and higher-cost models.

Mitigation: Review model and duration settings before submission, monitor credit usage, and prefer lower-cost models when appropriate.

Risk: The workflow depends on a secret API key and external network calls.

Mitigation: Store AIVIDEO_API_KEY in environment or secret storage, rotate it regularly, and do not hardcode it in skill archives or configuration files.

## Reference(s):

- [AIVideoMaker API Reference](references/api-reference.md)
- [Usage Examples](references/examples.md)
- [AIVideoMaker](https://aivideomaker.ai)
- [ClawHub Skill Page](https://clawhub.ai/rainlin10/skills/zxcvbnm-mnbvcxz)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime results are normalized with ok, status, taskId, data, errorCode, errorMessage, retryAfter, httpStatus, and timestamp fields.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and package files report 1.0.12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
