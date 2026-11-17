## Description:

Agent identity management with TAP protocol verification and reputation tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[efedurmaz16](https://clawhub.ai/user/efedurmaz16)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to register and verify AI agent identities, retrieve identity status, manage reputation scores, and generate shareable identity cards for agent marketplaces or transaction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit payment-linked agent identity and reputation data to an external Sardis service.

Mitigation: Use a scoped Sardis API key, confirm before registration or reputation POST requests, and avoid submitting sensitive comments or regulated transaction identifiers unless approved.

Risk: The release depends on Sardis API credentials and references the @sardis/sdk package.

Mitigation: Review installation before use and prefer a pinned, reviewed @sardis/sdk version.

## Reference(s):

- [Sardis Homepage](https://sardis.sh)
- [Sardis Identity Documentation](https://sardis.sh/docs/identity)
- [TAP Protocol Documentation](https://sardis.sh/docs/tap)
- [Sardis API Reference](https://api.sardis.sh/v2/docs)
- [ClawHub Skill Page](https://clawhub.ai/efedurmaz16/skills/sardis-identity)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SARDIS_API_KEY and the curl and jq command-line tools.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
