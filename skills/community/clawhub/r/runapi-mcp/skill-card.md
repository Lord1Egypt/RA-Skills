## Description:

Use RunAPI MCP tools to generate images, videos, music, audio, and speech, submit media tasks, and check task status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to route media generation requests through RunAPI, validate model parameters, create or poll tasks, and receive task IDs, statuses, output URLs, and cost fields when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RunAPI media task submission may incur costs.

Mitigation: Confirm video, music, or batch requests before task creation and present available cost fields when available.

Risk: Generated file URLs are temporary and valid for 7 days.

Mitigation: For durable use, download and store generated files in user-controlled storage.

Risk: The broad "check this task" trigger may activate on ambiguous requests.

Mitigation: Confirm the request concerns RunAPI task status before polling when the context is unclear.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with task identifiers, task status, output URLs, and cost fields when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [RunAPI-generated file URLs are temporary and valid for 7 days; durable workflows need separate storage.]

## Skill Version(s):

0.1.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
