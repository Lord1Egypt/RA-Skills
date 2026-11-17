## Description:

AI-powered healthcare knowledge management. Search clinical notes, care plans, lab results, prescriptions, and patient pathways with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare employees and administrators use this skill to search organizational healthcare knowledge for clinical protocols, care pathways, formulary decisions, quality metrics, credentialing criteria, and compliance documentation. It supports grounded summaries and workflow guidance from an authorized UPLO knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive healthcare and organizational knowledge access can cross PHI, credentialing, peer-review, or incident-investigation boundaries if access tiers are unclear.

Mitigation: Connect only to an authorized UPLO instance, enforce least-privilege healthcare access, and document PHI and privileged-record boundaries before production use.

Risk: Bulk organizational context export can disclose more information than a single protocol lookup requires.

Mitigation: Restrict or disable full context export unless the workflow requires it, and review export access separately from ordinary search access.

Risk: Runtime execution of an unpinned npm MCP package can introduce supply-chain drift.

Mitigation: Pin and review the MCP server version before production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/roojenkins/skills/uplo-healthcare)
- [UPLO](https://uplo.ai)
- [UPLO Schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline tool commands or configuration snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should cite the source protocol, revision date, and approving authority when healthcare knowledge is surfaced.]

## Skill Version(s):

1.0.0 (source: skill.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
