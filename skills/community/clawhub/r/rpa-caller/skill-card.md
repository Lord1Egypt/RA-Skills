## Description:

RPA Caller helps an agent trigger and monitor RPA automation through HTTP requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to map user requests to approved RPA HTTP endpoints, collect required parameters, show the request for confirmation, submit automation tasks, and report task status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger broad RPA actions against configurable HTTP endpoints using bearer tokens.

Mitigation: Use only controlled RPA servers over HTTPS, restrict calls to approved hosts and endpoints, and issue least-privilege short-lived tokens.

Risk: Request previews may expose sensitive parameters or high-privilege tokens in the conversation.

Mitigation: Redact secrets and sensitive form values before displaying requests, and avoid pasting high-privilege API keys into chat context.

Risk: Screenshots, form submission, file downloads, and stop or force-stop actions can affect systems or expose data.

Mitigation: Require explicit user confirmation for these actions and ensure RPA-side logging, authorization checks, and rollback procedures are in place.

## Reference(s):

- [RPA API Map](references/rpa-api-map.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured HTTP request details, JSON request bodies, and status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bearer-token authenticated HTTP request plans and task identifiers; sensitive values should be redacted before display.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
