## Description:

Extracts structured JSON from sea-shipping booking notes and shipping instructions in PDF, image, scanned, Word, Excel, and RTF formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucezhouzhou](https://clawhub.ai/user/brucezhouzhou)

### License/Terms of Use:

MIT-0

## Use Case:

External logistics teams and agents use this skill to turn uploaded shipping booking files into a standardized booking JSON, with low-confidence fields flagged for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive booking documents, including commercial and personal shipping details, can be sent to the configured AI provider.

Mitigation: Install only when that data transfer is acceptable and use a trusted provider endpoint.

Risk: OPENAI_BASE_URL can direct model requests to an untrusted host.

Mitigation: Avoid untrusted custom endpoints and configure only trusted provider URLs.

Risk: The skill can auto-read local OpenClaw auth profiles to find API credentials.

Mitigation: Review OpenClaw auth-profile access before use, especially in shared or sensitive environments.

Risk: Sensitive workflows may be affected by unpinned Python dependencies.

Mitigation: Use an isolated environment with pinned dependencies for production or sensitive document processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucezhouzhou/skills/shipping-booking)
- [Publisher profile](https://clawhub.ai/user/brucezhouzhou)
- [Booking Note Schema](artifact/references/schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Standardized JSON with optional human-review warnings in Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports low-confidence fields and rejects files that do not appear to be shipping booking documents.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
