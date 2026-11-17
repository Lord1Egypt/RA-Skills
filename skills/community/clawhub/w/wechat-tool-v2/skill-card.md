## Description:

Searches for WeChat public-account articles by keyword and reads article pages, returning titles, authors, links, snippets, and extracted body paragraphs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to locate WeChat public-account articles, extract article metadata and body text, and support downstream summarization, translation, analysis, or reporting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Web and browser fetch paths are broadly scoped.

Mitigation: Restrict outbound network access to intended WeChat domains and review requested URLs before use.

Risk: The Playwright screenshot option can write to arbitrary writable paths.

Mitigation: Disable screenshots unless needed, or constrain screenshot output to a dedicated low-risk directory.

Risk: The skill may run in environments with private-network or important writable-file access.

Mitigation: Run it as an unprivileged user in an isolated environment with only the minimum network and filesystem permissions required.

Risk: Runtime dependencies include web scraping and browser automation packages.

Mitigation: Pin dependencies and review package versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onlyloveher/skills/wechat-tool-v2)
- [Publisher profile](https://clawhub.ai/user/onlyloveher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional shell commands and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and read results can include article title, author, URL, digest, date, body paragraphs, read mode, and optional screenshot output.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
