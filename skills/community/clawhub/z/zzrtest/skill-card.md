## Description:

Searches and analyzes DEV environment transaction logs across procurement, platform, supplier, and order services, including supplier HTTP request/response extraction when supplier-side errors are detected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[extraskittles](https://clawhub.ai/user/extraskittles)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and authorized DEV operators use this skill to investigate test-environment transaction issues by searching layered service logs, tracing supplier routing, and extracting relevant request and response payloads for diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retrieve, store, and expose raw internal and supplier log payloads.

Mitigation: Install only for authorized DEV operators, treat outputs and cached files as sensitive, restrict local file permissions, and delete ~/.DEV_SKILL/dev-find-log run directories after use.

Risk: Personal devtool tokens may be used through the local configuration file.

Mitigation: Avoid pasting real tokens into chats or repositories and store local configuration only in the expected private cache location.

## Reference(s):

- [DEV Log System API Reference](references/api.md)
- [DEV Transaction Service Layers](references/service-layers.md)
- [ClawHub Skill Page](https://clawhub.ai/extraskittles/skills/zzrtest)
- [DEV Log Gateway](https://devtool.flightroutes24.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include execute IDs, service hit status, layered log analysis, and extracted HTTP request/response payloads.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
