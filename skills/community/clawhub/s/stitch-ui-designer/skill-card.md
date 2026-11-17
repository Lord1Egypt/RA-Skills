## Description:

Designs, previews, iterates on, and exports UI code using Google Stitch through MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a2mus](https://clawhub.ai/user/a2mus)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create UI concepts from text prompts, review preview images, refine designs, and export HTML/CSS after approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup runs an unpinned npm package through npx.

Mitigation: Review and pin the `stitch-mcp-auto` package version before configuring the MCP server.

Risk: The MCP process may use local Google Cloud authentication context.

Mitigation: Use a dedicated least-privilege Google Cloud project or account and review the mcporter configuration before running the skill.

## Reference(s):

- [Stitch UI Designer on ClawHub](https://clawhub.ai/a2mus/skills/stitch-ui-designer)
- [Publisher profile: a2mus](https://clawhub.ai/user/a2mus)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and HTML/CSS code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include UI preview image references or generated HTML/CSS after user approval.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
