## Description:

WeChat2PDF converts WeChat public-account articles into offline PDF, HTML, and Markdown files with images preserved for archiving and offline reading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xi0ng8](https://clawhub.ai/user/xi0ng8)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to preserve WeChat public-account articles for offline reading, sharing, or import into personal knowledge bases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports unsafe unrestricted fetching and rendering paths while the skill downloads article content and assets and writes local files.

Mitigation: Run only after explicit WeChat conversion requests, review output paths, and enforce a WeChat/CDN allowlist with private-network protections before use in sensitive environments.

Risk: The skill uses Chromium to render fetched content into PDF.

Mitigation: Pin dependencies and sanitize HTML or disable JavaScript and network access during rendering where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xi0ng8/skills/xi0ng8-wechat2pdf)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Guidance]

**Output Format:** [PDF, HTML, Markdown, local image assets, and concise Markdown status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local files from a supplied article URL and can report the output paths.]

## Skill Version(s):

0.1.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
