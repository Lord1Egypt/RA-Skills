## Description:

Fetches WeChat Work developer documentation pages through an authenticated session and converts the returned content into clean Markdown for local use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mouzhi](https://clawhub.ai/user/mouzhi)

### License/Terms of Use:


## Use Case:

Developers and technical writers use this skill to save authenticated WeChat Work developer documentation pages as Markdown, especially for Obsidian or local knowledge-base workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live WeChat Work session cookies in plaintext workflows.

Mitigation: Use short-lived, least-privileged sessions; avoid pasting real cookies into source files or shell history; remove or rotate exposed cookies.

Risk: The local script contacts developer.work.weixin.qq.com using the user's authenticated session.

Mitigation: Run it only in a trusted local environment, preferably inside a virtual environment with pinned dependency versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mouzhi/skills/wecom-doc-fetcher)
- [WeChat Work developer documentation](https://developer.work.weixin.qq.com/document/path/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local Markdown files or stdout text from fetched WeChat Work documentation content.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
