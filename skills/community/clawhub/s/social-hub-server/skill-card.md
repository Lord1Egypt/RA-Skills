## Description:

Social Hub Server is a centralized OpenClaw relationship-matching engine that coordinates profile updates, vector and LLM-based scoring, match notifications, confirmation workflows, and feedback among users' personal agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freeai-io](https://clawhub.ai/user/freeai-io)

### License/Terms of Use:


## Use Case:

External agents and operators use this skill to run a central matching service for a small social graph, coordinating profile ingestion, match evaluation, disclosure-filtered introductions, and feedback loops between personal agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill centralizes sensitive user profiles and relationship metadata.

Mitigation: Use only where all participants have agreed to centralized profile storage, and define retention and deletion controls before deployment.

Risk: Profile data may be sent to external AI processing for embeddings or matching evaluation.

Mitigation: Define approved AI providers and exclude or separately consent private fields before they are processed.

Risk: Shared-group logs may expose identifiable matching activity or operational details.

Mitigation: Restrict detailed logs to authorized staff and keep private profile fields out of observable messages.

Risk: Local profile, match-history, and vector data are retained under the match-engine data directory.

Mitigation: Protect the ~/.matchbot-engine directory with appropriate access controls and operational safeguards.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freeai-io/skills/social-hub-server)
- [ClawHub publisher profile](https://clawhub.ai/user/freeai-io)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with JSON message examples and scheduling configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes protocol-oriented status messages, match notifications, disclosure-filtered introduction content, and cron timing guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
