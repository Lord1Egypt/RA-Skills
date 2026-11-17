## Description:

Takes website screenshots, captures full pages, generates PDFs, and handles desktop, mobile, dark mode, stealth mode, cookie banner blocking, and batch URLs via the Allscreenshots cloud API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panilya](https://clawhub.ai/user/panilya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to capture screenshots or PDFs of websites without running a local browser, including desktop, mobile, full-page, viewport-only, and dark-mode variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive page URLs or resulting screenshots may be processed or stored by a third-party cloud API.

Mitigation: Do not submit internal, authenticated, regulated, or secret-bearing pages unless authorized and comfortable with the vendor's controls; prefer binary output over stored URL output for sensitive captures.

Risk: The Allscreenshots API key could be exposed through shared commands, logs, or configuration files.

Mitigation: Keep ALLSCREENSHOTS_API_KEY private, load it from local environment configuration, and avoid committing or sharing the key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/panilya/skills/website-capture)
- [Allscreenshots dashboard](https://dashboard.allscreenshots.com)
- [Allscreenshots screenshots API endpoint](https://api.allscreenshots.com/v1/screenshots)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown with bash and JSON examples; API responses may include image URLs, base64 JSON, binary image bytes, or PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and ALLSCREENSHOTS_API_KEY; captures are processed by the Allscreenshots cloud API.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
