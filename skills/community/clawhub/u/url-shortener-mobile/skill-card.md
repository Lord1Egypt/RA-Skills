## Description:

Guides an agent to shorten long URLs with public URL-shortening services and return a verified short link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmiu](https://clawhub.ai/user/tmiu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user asks to shorten, abbreviate, or create a shareable link from a long HTTP(S) URL. It guides the agent through public URL-shortening services, fallback handling, and validation of the returned short URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided URLs are sent to public URL-shortening services and may disclose sensitive links to those providers.

Mitigation: Do not use the skill for private intranet links, password reset links, signed URLs, links containing tokens, or personal-data URLs unless the user accepts that disclosure.

Risk: A failed or unexpected shortener response could produce an incorrect or misleading short link.

Mitigation: Validate that the returned URL starts with the expected shortener domain, use documented fallbacks, and report failure instead of fabricating a short URL.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tmiu/skills/url-shortener-mobile)
- [da.gd shortener endpoint](https://da.gd/s)
- [cleanuri shortening endpoint](https://cleanuri.com/api/v1/shorten)
- [TinyURL create endpoint](https://tinyurl.com/api-create.php)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Text]

**Output Format:** [Markdown or plain text guidance with HTTP request examples and plain text short URL output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the short URL only after validating that the response domain matches the selected public shortener.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
