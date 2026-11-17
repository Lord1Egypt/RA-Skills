## Description:

The Vibe VC helps an agent submit a vibe-coded startup to The Vibe VC, connect diligence integrations, and relay required human verification instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oliversum-ch](https://clawhub.ai/user/oliversum-ch)

### License/Terms of Use:

MIT-0

## Use Case:

External founders and their agents use this skill to prepare and submit startup registration details to The Vibe VC, connect diligence surfaces such as repositories, analytics, or billing, and relay required human verification instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive founder, project, repository, analytics, billing, and contact details may be disclosed to Vibe VC endpoints.

Mitigation: Get explicit human consent, review dry-run output before submission, keep requests limited to documented Vibe VC HTTPS hosts, and omit secrets or private contact data unless intentionally shared.

Risk: The skill relays remote social-post instructions for LinkedIn or X.

Mitigation: Have the human manually review and approve any social-post wording before publishing.

## Reference(s):

- [Vibe VC API + workflow reference](references/vibevc-api.md)
- [Canonical Vibe VC skill reference](https://vibevc.md/skill.md)
- [The Vibe VC public site](https://vibevc.md/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform HTTPS API calls to Vibe VC endpoints when the human consents; dry-run mode can print payloads before submission.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
