## Description:

AI-ready skill to extract long-form X (Twitter) articles and convert them into clean Markdown files using headless browser technology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caol64](https://clawhub.ai/user/caol64)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill when a user provides an X article URL and asks to save, read, extract, or convert long-form content into Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package installation and first-run browser dependency downloads involve normal third-party Python and browser code execution risk.

Mitigation: Install only where outbound network access and third-party code execution are acceptable; pin and verify package and browser dependencies where stronger control is required.

Risk: Extraction depends on outbound access to x.com and Playwright binary mirrors, which can fail in restricted environments.

Mitigation: Run the extractor in a sandbox with minimal filesystem access and no unnecessary secrets, and confirm required network access before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caol64/skills/x-article-to-markdown)
- [Repository listed in skill documentation](https://github.com/caol64/omni-article-markdown)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown files with preserved image URLs and converted quoted-post links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an X article URL and can accept an optional output directory; first execution may download Playwright and Chromium dependencies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
