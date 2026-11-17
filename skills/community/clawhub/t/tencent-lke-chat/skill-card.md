## Description:

Guides agents in calling Tencent Cloud LKE's HTTP SSE chat API, including sending messages, handling streaming responses, and parsing reply, token_stat, reference, error, and thought events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijiayi980130](https://clawhub.ai/user/lijiayi980130)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to integrate agents with Tencent Cloud LKE conversations over HTTP SSE and understand request parameters, streaming event parsing, model selection, and error handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, AppKeys, file URLs, document content, and other request values may leave the local environment for Tencent Cloud processing.

Mitigation: Use the skill only for Tencent Cloud LKE workflows approved by the organization, and avoid regulated personal data, internal document URLs, confidential prompts, and secrets unless policy permits that processing.

Risk: The example client may print session IDs, visitor IDs, selected system role text, custom variables, file counts, and reference URLs to stdout.

Mitigation: Avoid passing sensitive values through fields that may be logged, or redact and suppress logs before production use.

Risk: The dependency guidance does not pin Python package versions.

Mitigation: Pin and review dependency versions before production use.

Risk: The example script's optional JSON argument handling may exit early when optional JSON arguments are omitted.

Mitigation: Test the script with representative arguments and adjust optional argument handling before relying on it in automation.

## Reference(s):

- [HTTP SSE API Reference](references/api_reference.md)
- [Example SSE Chat Script](scripts/sse_chat.py)
- [Runtime Requirements](references/requirements.txt)
- [Tencent Cloud LKE SSE Endpoint](https://wss.lke.cloud.tencent.com/v1/qbot/chat/sse)
- [ClawHub Skill Page](https://clawhub.ai/lijiayi980130/skills/tencent-lke-chat)
- [Publisher Profile](https://clawhub.ai/user/lijiayi980130)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documentation with JSON examples, cURL commands, and Python example code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request fields, SSE event descriptions, model names, error codes, and optional Python command-line usage.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
