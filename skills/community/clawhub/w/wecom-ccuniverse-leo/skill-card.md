## Description:

Creates and edits WeCom documents and smart sheets through the wecom-doc MCP server using mcporter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boge-net](https://clawhub.ai/user/boge-net)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to create WeCom documents or smart sheets by default for document requests, then add content, sub-sheets, fields, and records through mcporter-mediated MCP calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install persistent tooling through npm.

Mitigation: Install only after reviewing the mcporter package source and approving the package for the target environment.

Risk: A user-provided StreamableHttp URL or JSON config may route document content to an untrusted service.

Mitigation: Use only official or enterprise-approved HTTPS MCP endpoints and reject unknown configuration URLs.

Risk: Document edit operations may overwrite existing content.

Mitigation: Confirm the target document ID and preserve or read existing content before applying full-document edits.

## Reference(s):

- [Enterprise WeCom document API reference](references/doc-api.md)
- [ClawHub skill page](https://clawhub.ai/boge-net/skills/wecom-ccuniverse-leo)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcporter and a configured wecom-doc MCP endpoint; document edits may overwrite content and depend on document IDs created during the session.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
