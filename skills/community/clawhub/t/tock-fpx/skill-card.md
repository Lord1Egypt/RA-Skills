## Description:

Query Tock restaurant discovery, availability, and signed-in reservation data from a shell using the fpx CLI and a paired browser tab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use this skill to inspect Tock metros, search restaurants, view venue availability, and list reservations from scripts without running the Tock MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authenticated reservation example can leave personal details in a predictable temporary file.

Mitigation: Filter the response directly, or use a private temporary directory and clean it up afterward.

Risk: A paired browser bridge can grant access through its approved site and capabilities.

Mitigation: Approve only the Tock domain and capabilities needed, then revoke pairing when finished.

Risk: The review covers bundled files, not the external CLI and browser extension releases.

Mitigation: Review the CLI and extension versions separately before use.

## Reference(s):

- [Tock request examples](artifact/references/requests.md)
- [Redux state extraction helper](artifact/references/extract-redux-slice.mjs)
- [ContextMint Bridge source](https://github.com/nullnet-app/contextmint-bridge)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [Tock](https://www.exploretock.com)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with shell command examples, jq filters, and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Tock queries; reservation history requires a signed-in browser tab.]

## Skill Version(s):

1.2.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
