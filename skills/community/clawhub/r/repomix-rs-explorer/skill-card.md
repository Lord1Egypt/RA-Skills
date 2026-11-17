## Description:

Pack a local or remote codebase with repomix-rs and analyze the generated output. Invoke for high-level exploration, structure summaries, or pattern discovery when targeted edits are not needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sopaco](https://clawhub.ai/user/sopaco)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to pack unfamiliar local or remote repositories with repomix-rs, inspect structure and metrics, search broad patterns, and summarize findings before deciding whether targeted file reads or edits are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm or npx execution, including auto-confirmed MCP startup, can introduce supply-chain and local-access risk.

Mitigation: Pin and review the repomix-rs package version before installing or running it, avoid npx -y until package provenance is trusted, and do not run the commands with elevated privileges.

Risk: Repository packing can collect secrets or unrelated private data from the selected directory.

Mitigation: Pack only intended directories, use include and ignore filters for narrow scope, and avoid packing repositories that contain secrets or unrelated private data.

## Reference(s):

- [repomix-rs repository](https://github.com/sopaco/repomix-rs)
- [repomix-rs npm package](https://www.npmjs.com/package/repomix-rs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with command examples and concise analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to create temporary repomix output files and summarize repository metrics, structure, and discovered patterns.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
