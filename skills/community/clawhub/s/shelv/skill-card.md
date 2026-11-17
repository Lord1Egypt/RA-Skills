## Description:

Convert PDFs into structured Markdown filesystems and hydrate them into your workspace for exploration with standard Unix tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joshuaohanlon](https://clawhub.ai/user/joshuaohanlon)

### License/Terms of Use:


## Use Case:

Developers and knowledge workers use this skill to upload PDF documents to Shelv, wait for remote processing, and hydrate the resulting Markdown file tree into an OpenClaw workspace for inspection with standard Unix tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected PDFs and the Shelv API key are sent to Shelv's remote service.

Mitigation: Use the skill only for documents approved for remote processing, and avoid confidential or regulated PDFs unless the organization has approved that use.

Risk: Hydrating with --force can replace an existing local shelf directory.

Mitigation: Review the shelf ID, derived or overridden shelf name, and target path before using --force.

Risk: Approve, regenerate, retry, and delete-style API operations can change remote shelf state.

Mitigation: Confirm the shelf ID and current status before issuing state-changing requests.

Risk: Downloaded archives write files into the local OpenClaw workspace.

Mitigation: Keep checksum verification, path traversal checks, and symlink rejection enabled before extraction.

## Reference(s):

- [Shelv](https://shelv.dev)
- [Shelv Documentation](https://docs.shelv.dev)
- [API Reference](references/api-reference.md)
- [Shelf Lifecycle](references/shelf-lifecycle.md)
- [Error Handling](references/error-handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and hydrated workspace files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SHELV_API_KEY and local curl, tar, jq, and shasum or sha256sum. Hydrated shelves are written under ~/.openclaw/workspace/shelves/<name>/.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
