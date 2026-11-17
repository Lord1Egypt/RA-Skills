## Description:

AI video generation workflow on Volcengine for text-to-video, image-to-video, generation parameter tuning, and async task troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to submit and monitor Volcengine text-to-video or image-to-video generation jobs, tune generation parameters, and troubleshoot asynchronous job failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video prompts or source images may be sent to Volcengine.

Mitigation: Confirm the user's Volcengine configuration and policy permit the submission, and avoid sensitive media unless it is approved for that provider.

Risk: Video generation jobs and retries may consume provider quota or incur costs.

Mitigation: Monitor Volcengine account limits and costs before running or retrying generation jobs.

## Reference(s):

- [Sources](references/sources.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured task details and inline commands or configuration when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include final video URL or path, task ID, status metadata, and failure reason.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
