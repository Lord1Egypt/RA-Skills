## Description:

Web to Markdown converts web pages to clean Markdown, extracts image URLs, and batch-downloads images from websites using conversion services and local fallback scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephxie1](https://clawhub.ai/user/josephxie1)

### License/Terms of Use:


## Use Case:

Developers, researchers, and agents use this skill to turn web pages into readable Markdown and collect image URLs or image files for content review, article reading, image collection, and source organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied URLs may be sent to third-party conversion services.

Mitigation: Avoid private, internal, authenticated, signed, or token-bearing URLs and get explicit confirmation before processing sensitive pages.

Risk: The skill can fetch or download arbitrary web content.

Mitigation: Run it in a constrained environment, review target URLs before execution, and apply download limits and destination controls.

Risk: Downloaded images and scraped content may come from untrusted websites.

Mitigation: Review downloaded files before reuse and keep normal malware scanning and content handling controls in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/josephxie1/skills/web-to-markdown)
- [markdown.new conversion service](https://markdown.new/)
- [defuddle.md conversion service](https://defuddle.md/)
- [r.jina.ai conversion service](https://r.jina.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown guidance with shell commands and plain-text URL lists or downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external conversion services, make arbitrary web requests, and write downloaded images to local storage.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
