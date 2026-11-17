## Description:

Generates OpenAPI 3.0 specs from endpoint descriptions for API validation, documentation, YAML formatting, schema checks, and contract linting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and API engineers use this skill when drafting or validating OpenAPI/Swagger contract material from endpoint descriptions. Review generated or stored content carefully because server security evidence reports a mismatch between advertised OpenAPI generation and executable behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Executable behavior may not perform the advertised OpenAPI generation and may instead log, search, and export user-supplied text.

Mitigation: Review the implementation before installation and require behavior changes that perform the advertised OpenAPI work before using it in production workflows.

Risk: User-supplied API descriptions, schemas, endpoints, or examples may be retained in local files.

Mitigation: Do not use private API contracts, credentials, internal endpoints, customer examples, or proprietary schemas unless retention is removed or clearly gated behind opt-in with redaction, deletion, and file-permission controls.

Risk: Sensitive content may remain on disk after prior use.

Mitigation: Inspect and remove sensitive files under ~/.local/share/swagger-generator if the skill has already been used.

## Reference(s):

- [Swagger Generator ClawHub Page](https://clawhub.ai/xueyetianya/skills/swagger-generator)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with YAML, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist user-supplied text to local history and export files under ~/.local/share/swagger-generator.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
