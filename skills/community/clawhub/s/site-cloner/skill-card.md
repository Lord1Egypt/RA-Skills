## Description:

Clone any live website into a self-contained, dependency-free HTML file with all content, styles, fonts, and images extracted and preserved.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michelle447](https://clawhub.ai/user/michelle447)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to recreate permitted websites as standalone HTML, including static pages and React, Vue, or Angular SPAs whose content is extracted from bundles. It can also guide optional publication to a private GitHub repository or VPS when the user has confirmed an authorized destination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can copy live websites, which can create legal, policy, or content ownership issues when used without permission.

Mitigation: Use it only for sites the user owns or is explicitly authorized to copy, and require the user to confirm permission before fetching, cloning, or publishing.

Risk: Optional deployment guidance uses a fixed third-party VPS destination and root-level remote administration.

Mitigation: Require user-provided deployment hosts, keys, paths, and ports, and use a least-privileged deployment account instead of root.

Risk: Optional GitHub publishing can push cloned site output to a repository destination.

Mitigation: Require explicit user confirmation of the repository owner, repository name, visibility, and remote URL before running GitHub publishing commands.

## Reference(s):

- [HTML Clone Template Guide](references/html-template.md)
- [SPA Bundle Extraction Guide](references/spa-extraction.md)
- [ClawHub skill page](https://clawhub.ai/michelle447/skills/site-cloner)
- [Publisher profile](https://clawhub.ai/user/michelle447)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline PowerShell, HTML, CSS, JavaScript, Git, SSH, and nginx configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local file paths, optional GitHub and VPS URLs, and an image download count when those actions are performed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
