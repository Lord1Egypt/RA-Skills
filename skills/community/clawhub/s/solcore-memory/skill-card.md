## Description:

Provides persistent, scored memory storage, behavioral pattern detection, context retrieval, and reflection analysis for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelandsol](https://clawhub.ai/user/michaelandsol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to give agents persistent memory, retrieve relevant past context, and analyze behavior patterns across interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and retrieves raw conversation content as long-term memory, which can expose secrets, regulated data, or private business content.

Mitigation: Install only where users intentionally want persistent memory, avoid sensitive content, and define consent, redaction, retention, and deletion controls before production use.

Risk: Retrieved memories can cross trust boundaries and influence later agent responses.

Mitigation: Treat retrieved memories as untrusted context, validate important claims before use, and restrict the SolCore webhook and PostgreSQL database to trusted operators.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/michaelandsol/skills/solcore-memory)
- [Publisher profile](https://clawhub.ai/user/michaelandsol)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [Plain text tool results and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on a configured SolCore webhook and PostgreSQL database.]

## Skill Version(s):

1.0.0 (source: server release metadata, openclaw.plugin.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
