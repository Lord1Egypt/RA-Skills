## Description:

Routes calls to api.a7w.cn as a unified AI gateway for 75 available models and 21 generation apps, with OpenAI-compatible model calls, async app tasks, authentication, billing guidance, callbacks, error handling, and a zero-dependency client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Developers and builders use this skill to connect agents or applications to api.a7w.cn with one API key, discover supported models and apps, call OpenAI-compatible chat endpoints, submit generation tasks, and troubleshoot billing or API errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security scan reports that the client can send a user API key to an arbitrary host when host overrides are used, despite documentation claims that it only contacts api.a7w.cn.

Mitigation: Use a dedicated low-quota API key, keep the host set to the default api.a7w.cn, avoid untrusted --host, A7W_HOST, or saved host settings, and rotate the key if it was ever used with an unintended host.

Risk: The skill calls paid AI services and async task submissions may reserve or consume points.

Mitigation: Review pricing and schema information before batch use, set key-level quotas, check task status before resubmitting after timeouts, and use tenant-specific price fields for budgeting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2253128/skills/sanjianke-one-key-ai-gateway)
- [OpenAPI definition](openapi.json)
- [Getting started](references/getting-started.md)
- [OpenAI-compatible model gateway](references/api-openai-compat.md)
- [Application tasks and async lifecycle](references/api-apps-tasks.md)
- [Billing, budgeting, and errors](references/api-billing-errors.md)
- [Client CLI manual](references/client-cli.md)
- [api.a7w.cn](https://api.a7w.cn/)
- [AI plugin marketplace](https://aigc.a7w.cn/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API calls, JSON]

**Output Format:** [Markdown guidance with shell commands, Python snippets, OpenAPI JSON, and CLI JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled client can save JSON responses only when explicitly given an output path.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
