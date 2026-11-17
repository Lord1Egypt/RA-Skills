## Description:

AI-powered education knowledge management. Search curriculum documents, student records frameworks, accreditation data, and institutional research with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Education administrators, faculty, institutional researchers, and accreditation teams use this skill to search institution-specific curriculum, assessment, accreditation, policy, and student success knowledge and assemble grounded evidence for reviews or reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm MCP server while passing a sensitive UPLO API token.

Mitigation: Install only from a trusted UPLO/npm source, pin and review the MCP server version, and use a least-privilege UPLO token scoped to the required education datasets and operations.

Risk: Queries or exports can include student-identifiable or confidential institutional information.

Mitigation: Respect classification tiers, confirm authorization before exporting organizational context, and restrict access to the user's institutional role and clearance.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/roojenkins/skills/uplo-education)
- [UPLO](https://uplo.ai)
- [UPLO schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline tool, shell command, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use configured UPLO education knowledge access to retrieve, flag, export, or propose updates to institutional context.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
