## Description:

Web Tools helps agents search and extract web content, analyze page performance, deploy static sites, and convert files to Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cooperiano](https://clawhub.ai/user/cooperiano)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to research web pages, extract readable content, audit page performance, publish static sites to GitHub Pages, and convert common document and media formats to Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub Pages deployment could publish the wrong folder, repository, or private content if approved without review.

Mitigation: Before deployment, confirm the target folder, repository or account, commit contents, and that secrets or private files are excluded.

Risk: Web extraction and performance analysis may touch pages that should not be crawled or audited.

Mitigation: Use the skill only on pages the user is authorized to access, and avoid login walls, key exposure, and malicious security testing.

## Reference(s):

- [Web Tools on ClawHub](https://clawhub.ai/cooperiano/skills/web-tools)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with code or shell command snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
