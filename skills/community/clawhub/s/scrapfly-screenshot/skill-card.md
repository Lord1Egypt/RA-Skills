## Description:

Capture web page screenshots using the Scrapfly Screenshot API with the Python SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scrapfly](https://clawhub.ai/user/scrapfly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to capture full-page, viewport, element-specific, geo-targeted, or JavaScript-rendered screenshots of web pages through Scrapfly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs, rendered page content, and screenshots may be sent to or stored by Scrapfly.

Mitigation: Use the skill only with pages approved for third-party processing, and avoid private, authenticated, internal, or regulated content unless organizational approval covers that sharing and retention.

Risk: The Scrapfly API key could be exposed if placed directly in prompts, code, or logs.

Mitigation: Provide the key through SCRAPFLY_API_KEY or an approved secret store, and avoid hard-coding credentials in generated examples.

Risk: Custom JavaScript execution before capture can change what is rendered or remove page elements unintentionally.

Mitigation: Review any custom JavaScript and selectors before use, and scope them to the intended page elements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scrapfly/skills/scrapfly-screenshot)
- [Scrapfly Screenshot API endpoint](https://api.scrapfly.io/screenshot)
- [Scrapfly Python SDK screenshot configuration](https://raw.githubusercontent.com/scrapfly/python-scrapfly/master/scrapfly/screenshot_config.py)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to call the Scrapfly Screenshot API and save returned image files; requires a Scrapfly API key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
