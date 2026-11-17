## Description:

Skroll helps agents write, publish, version, and export presentation decks by authoring a React/TSX module and sending it through the Skroll CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benlaval23](https://clawhub.ai/user/benlaval23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and presentation authors use this skill to create, update, publish, version, and export Skroll decks from the terminal. It is suited for pitch decks, slide presentations, reusable templates, and PDF or PPTX export workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on unpinned npm CLI execution for authenticated deck operations.

Mitigation: Run a reviewed pinned CLI version or locked local install before using it with Skroll credentials.

Risk: The workflow can upload local file contents through `@file` arguments.

Mitigation: Review file paths and contents before passing them to the CLI, and avoid including secrets or unrelated local data.

Risk: The CLI supports publishing and deletion actions that can affect deck availability.

Mitigation: Confirm target deck IDs, visibility changes, and delete operations before execution; prefer archiving when appropriate.

Risk: Authentication tokens or API keys grant access to Skroll operations.

Mitigation: Use least-privilege, revocable credentials and rotate or revoke them when no longer needed.

## Reference(s):

- [Skroll](https://skrollai.com)
- [Skroll CLI Documentation](https://skrollai.com/developers/cli)
- [Skroll MCP Documentation](https://skrollai.com/developers/mcp)
- [Skroll REST Documentation](https://skrollai.com/developers)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands and React/TSX module authoring; CLI operations may return JSON or downloaded PDF/PPTX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 22+, network access to skrollai.com, and Skroll authentication through browser login, SKROLL_API_KEY, or SKROLL_TOKEN.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
