## Description:

Uses Puppeteer and local Chrome to fetch WeChat public-account articles, extract article text and metadata, and optionally save the result as Markdown, HTML, or plain text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adgai115](https://clawhub.ai/user/adgai115)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-operations users can use this skill to extract accessible WeChat article content, metadata, and images into local files for review, archiving, or downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches a local browser with browser sandbox disabled against caller-supplied article URLs.

Mitigation: Use only trusted WeChat article URLs and run the skill in a restricted environment without access to sensitive local or private-network services.

Risk: The skill can download page-selected images without adequate limits.

Mitigation: Disable image downloads unless needed, monitor output size, and review downloaded files before using them downstream.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adgai115/skills/wechat-article-fetcher-safe)
- [Artifact README](artifact/README.md)
- [Artifact Skill Documentation](artifact/SKILL.md)
- [Artifact GitHub README](artifact/README.github.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Configuration]

**Output Format:** [Console text plus optional Markdown, HTML, plain-text, image, and JSON manifest files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, puppeteer-core, and a local Chrome or Chromium executable.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
