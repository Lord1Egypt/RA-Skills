## Description:

TreeListy helps agents decompose complex projects, structure nested information, and export hierarchical plans as JSON, Markdown, Mermaid, CSV, checklist, or HTML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prairie2cloud](https://clawhub.ai/user/prairie2cloud)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers, planners, and content authors use TreeListy to turn topics, outlines, and complex goals into hierarchical project structures, validate tree quality, and export results for documentation or diagrams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional push command can send tree data and a token over unencrypted WebSocket to a configured host.

Mitigation: Use push only with localhost or trusted loopback endpoints, and avoid sending sensitive tree contents until destination restrictions or authenticated encrypted transport are available.

Risk: CSV exports can be risky when opened in spreadsheet software.

Mitigation: Treat generated CSV files as untrusted content and inspect or sanitize spreadsheet formulas before opening them.

Risk: The security guidance calls for updating the ws dependency.

Mitigation: Update ws before deployment and rerun dependency and security scans.

Risk: The freespeech pattern can analyze personal speech transcripts.

Mitigation: Use the freespeech pattern only with informed consent from anyone whose transcript is being analyzed.

## Reference(s):

- [TreeListy Pattern Reference](references/PATTERNS.md)
- [TreeListy Web App](https://treelisty.com)
- [ClawHub Skill Page](https://clawhub.ai/prairie2cloud/skills/treelisty-openclaw-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON, Markdown, Mermaid, CSV, checklist, HTML, and plain-text validation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Node.js CLI outputs; optional WebSocket push to a TreeListy browser session.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
