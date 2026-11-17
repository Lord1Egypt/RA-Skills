## Description:

Provides temporary email receiving functionality using the Temporam API for generating temporary addresses, listing received emails, retrieving email content, and polling the latest email for an address.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shulkme](https://clawhub.ai/user/shulkme)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to generate disposable email addresses and read incoming temporary-mail messages for verification flows, sign-up testing, and temporary communication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Retrieved emails, verification codes, message metadata, and full message contents may be sensitive.

Mitigation: Use the skill only in isolated environments and avoid sensitive, regulated, or personal communications unless Temporam handling is acceptable.

Risk: The TEMPORAM_API_KEY may be exposed or over-scoped if shared across environments.

Mitigation: Use a scoped API key, keep it in the environment rather than prompts or logs, and rotate it after use.

Risk: External Temporam API calls and unpinned dependencies can create reliability and supply-chain risk in production.

Mitigation: Pin dependencies and add request timeouts before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shulkme/skills/temporam-skill)
- [Temporam API Reference](https://www.temporam.com/docs/api-reference)
- [Project homepage](https://github.com/shulkme/temporam-skill)
- [Support issues](https://github.com/shulkme/temporam-skill/issues)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [MCP tool responses, Python return values, and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TEMPORAM_API_KEY and calls the Temporam API to return generated addresses, email metadata, and full message content.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact frontmatter, changelog, and clawhub.json report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
