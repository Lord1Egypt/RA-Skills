## Description:

Entry skill for Volcengine ARK model invocation and routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to start Volcengine ARK chat-completion requests, route task types to a suitable workflow, and troubleshoot endpoint, authentication, rate-limit, and service errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, API keys, or private data may be sent to the Volcengine ARK endpoint.

Mitigation: Treat ARK_API_KEY as sensitive and avoid sending secrets or private data unless the ARK account and data-handling requirements allow it.

Risk: Requests can fail when the endpoint region, endpoint ID, API key scope, or request rate is incorrect.

Mitigation: Verify endpoint and key configuration, reduce request rate when needed, and retry transient service errors with jitter while keeping request logs for support.

## Reference(s):

- [Skill source references](references/sources.md)
- [Volcengine ARK chat completions endpoint](https://ark.cn-beijing.volces.com/api/v3/chat/completions)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and request JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ARK API key, endpoint ID, task type, optional generation parameters, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata, published 2026-02-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
