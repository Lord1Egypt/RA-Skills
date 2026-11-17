## Description:

Show your verified WayID identity card when a user asks who you are, who owns you, who runs you, or asks to see proof of identity, ownership, or provenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lineagelabs](https://clawhub.ai/user/lineagelabs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to display a WayID identity card for an agent, including the agent name, owner profile, verification status, and certificate link returned by the WayID issuer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can present verified ownership based on a locally configured issuer and a remote response.

Mitigation: Protect wayid.json from modification, use only issuers the operator intentionally trusts, and verify certificate links before relying on the displayed identity.

Risk: The optional plugin alternative changes execution behavior outside the Markdown skill instructions.

Mitigation: Avoid installing the optional plugin unless the exact package version can be pinned and reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lineagelabs/skills/whoareyou)
- [WayID](https://way.je)
- [WayID Claim Skill](https://way.je/claim/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown identity card with certificate link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a local wayid.json DID record, performs one HTTPS GET to the configured WayID issuer, and renders only fields returned by the API.]

## Skill Version(s):

3.3.0 (source: frontmatter and changelog, released 2026-06-08)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
