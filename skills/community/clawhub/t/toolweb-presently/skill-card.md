## Description:

AI-powered API for generating structured presentations from text input with customizable themes and formatting options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, educational platforms, and SaaS applications use this skill to turn source text into structured presentation slides with configurable card count, themes, and colors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source text and optional user identifiers are sent to ToolWeb's external API.

Mitigation: Do not submit secrets, credentials, regulated data, or unnecessary personal email addresses in presentation input.

Risk: Generated slide decks may omit nuance or introduce misleading summaries from the source text.

Mitigation: Review generated slides before sharing or using them for decisions.

## Reference(s):

- [ClawHub Presently skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-presently)
- [Presently API route](https://api.toolweb.in/tools/presently)
- [Presently API docs](https://api.toolweb.in:8174/docs)
- [Bundled OpenAPI specification](artifact/openapi.json)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON API responses with structured slide card data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a presentation identifier, status, slide cards with titles and content, applied theme, colors, and creation timestamp.]

## Skill Version(s):

1.0.0 (source: release evidence and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
