## Description:

Send X5 protocol API requests from the terminal, parse .x5 multi-request files, generate X5-compliant cURL commands, and debug X5 service endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[growingppp](https://clawhub.ai/user/growingppp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to send, inspect, and debug X5 protocol API requests from inline parameters or .x5 request files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles X5 app IDs, app keys, request bodies, and arbitrary target URLs.

Mitigation: Avoid putting real app keys on the command line or in shared .x5 files, and verify each destination URL before sending a request.

Risk: Listing, dry-run, JSON, and generated cURL output can expose request data or secrets from .x5 files.

Mitigation: Do not run listing or debug modes on files containing secrets, and manually review generated cURL output from untrusted .x5 files before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/growingppp/skills/x5-protocol)
- [Publisher profile](https://clawhub.ai/user/growingppp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, and generated command text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include encoded request previews, parsed request listings, cURL commands, and JSON response summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata and user-provided changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
