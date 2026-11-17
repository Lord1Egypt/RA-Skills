## Description:

Tencent Ima Skill Publish lets an agent work with Tencent IMA notes and knowledge bases, including search, browse, create, append, URL import, and file upload workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wat2012](https://clawhub.ai/user/wat2012)

### License/Terms of Use:

MIT-0; upstream Tencent IMA OpenAPI terms apply to original package content

## Use Case:

External users and developers use this skill to let an agent manage Tencent IMA note and knowledge-base content through official OpenAPI credentials. It is intended for personal or team knowledge workflows that need command, API, and guidance outputs for read/write IMA operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires IMA OpenAPI credentials with note and knowledge-base read/write access.

Mitigation: Install only for trusted publishers, inject credentials through tightly permissioned environment handling, and prevent the agent from printing or reading credential files aloud.

Risk: The security evidence flags unsafe credential handling and warns against IMA_BASE_URL or HERMES_ENV overrides.

Mitigation: Keep requests constrained to ima.qq.com and scoped COS endpoints, and avoid setting IMA_BASE_URL or HERMES_ENV unless reviewed.

Risk: Remote update instructions returned by the service may be untrusted display text.

Mitigation: Treat update instructions as advisory text for human review and do not execute or follow them automatically.

Risk: Write operations can create or upload content that the OpenAPI cannot later delete, move, or rename.

Mitigation: Use the documented preflight, duplicate-name checks, upload gates, and manual review before write operations; use the IMA client for unsupported cleanup.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wat2012/skills/tencent-ima-hermes)
- [Publisher profile](https://clawhub.ai/user/wat2012)
- [Tencent IMA homepage](https://ima.qq.com)
- [Tencent IMA OpenAPI credential page](https://ima.qq.com/agent-interface)
- [Official Tencent IMA OpenAPI skill package](https://app-dl.ima.qq.com/skills/ima-skills-1.1.7.zip)
- [Knowledge-base API reference](knowledge-base/references/api.md)
- [Notes API reference](notes/references/api.md)
- [IMA write-flow recipe](references/ima-write-flow.md)
- [IMA OpenAPI quirks](references/api-quirks.md)
- [Official endpoint coverage](references/official-endpoint-coverage.md)
- [Post-upload validation](references/post-upload-validation.md)
- [IMA write hard gates](references/ima-write-hard-gates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke Tencent IMA API calls and local helper scripts when used by an agent with credentials.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
