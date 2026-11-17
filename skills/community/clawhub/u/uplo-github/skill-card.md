## Description:

AI-powered GitHub knowledge management. Search repository metadata, code review standards, issue tracking, and team workflows with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to query organization-specific GitHub repository metadata, CODEOWNERS mappings, issue and pull request history, code review standards, and team workflow context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned downloaded MCP server and uses an API token that may access broad organizational context.

Mitigation: Review before installing, use a short-lived least-privilege UPLO token, avoid shared configs, prefer a pinned or verified MCP server version, and run with limited local filesystem and environment access.

Risk: GitHub information may reflect the last UPLO ingestion snapshot rather than live GitHub state.

Mitigation: Verify time-sensitive CI status, latest commits, permissions, and issue or pull request state directly in GitHub before acting.

Risk: Organizational context exports, repository metadata, and team information may be sensitive.

Mitigation: Respect classification tiers, limit export and sharing of organization context, and never surface access tokens or deployment credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/roojenkins/skills/uplo-github)
- [UPLO](https://uplo.ai)
- [UPLO Schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text responses grounded in UPLO GitHub knowledge queries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository names, team handles, relevant links, ownership details, review requirements, issue context, directives, and stale-entry flags.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
