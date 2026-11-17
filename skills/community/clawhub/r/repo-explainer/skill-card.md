## Description:

Repo Explainer analyzes a public GitHub repository or local code directory and produces source-grounded HTML and Markdown reports for non-developer readers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoloyyh](https://clawhub.ai/user/yoloyyh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering-adjacent stakeholders use this skill to turn public GitHub repositories or local code directories into source-grounded explanatory reports. The reports help PMs, designers, managers, and engineers understand purpose, architecture, key modules, data flow, dependencies, and limitations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports can expose private source details when run on local workspaces or overly broad directories.

Mitigation: Run the skill only on intended repositories or focused subpaths, and review generated HTML and Markdown before sharing.

Risk: Security evidence flags unsafe script-rendering behavior in the HTML report around Mermaid rendering.

Mitigation: Treat generated HTML as untrusted, prefer Markdown for broad sharing, and open HTML reports only from trusted runs until Mermaid escaping or bundling is fixed.

Risk: Broad home or sensitive monorepo scans may include more source data than intended because subpath enforcement and symlink handling need review.

Mitigation: Use explicit subpaths for monorepos and avoid pointing the skill at broad personal or work directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yoloyyh/skills/repo-explainer)
- [Mermaid.js](https://mermaid.js.org/)
- [GitHub REST API v3](https://docs.github.com/en/rest)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [HTML and Markdown report files with Mermaid diagrams and path:line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The HTML report is themed and single-file; the Markdown report uses native Mermaid code blocks for sharing in documentation and collaboration tools.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
