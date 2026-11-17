## Description:

Generate and read XMind (.xmind) files via the published xmind-generator-mcp MCP server (npm), with a chat-first UX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bangyizhang](https://clawhub.ai/user/bangyizhang)

### License/Terms of Use:


## Use Case:

Developers, knowledge workers, and agents use this skill to turn outlines, plans, PRDs, and test plans into real .xmind files, or to read an existing XMind file and summarize its structure and key points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs the pinned third-party xmind-generator-mcp npm package through npx.

Mitigation: Install only in environments where running that package is acceptable, and review the package before use in sensitive workflows.

Risk: Generated files may be saved to the Desktop by default, and sensitive mind-map content may be passed to the MCP process.

Mitigation: Specify an explicit output folder and use a sandboxed or low-privilege agent environment with access only to intended files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bangyizhang/skills/xmind-skill)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated .xmind files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a Markdown export when reading an XMind file.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
