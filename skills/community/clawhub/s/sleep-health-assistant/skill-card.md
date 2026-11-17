## Description:

Provides local, science-based analysis of sleep and stress with personalized guidance in relaxation, breathing, mindfulness, and wellness habits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[znsyhandao](https://clawhub.ai/user/znsyhandao)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill for local sleep and stress self-assessment, wellness habit suggestions, guided breathing, mindfulness, relaxation, and session cleanup. It is intended for general wellness education and self-improvement, not medical advice, diagnosis, or treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wellness analysis may be mistaken for medical advice.

Mitigation: Treat outputs as general wellness education and consult a healthcare professional for medical concerns.

Risk: Sensitive health details are temporarily held in memory during a session.

Mitigation: Use the cleanup command after entering sensitive health details, especially in shared or long-running OpenClaw sessions.

Risk: Install examples are not pinned to an immutable version.

Mitigation: Install only from a trusted ClawHub source and prefer a pinned version or verified package when available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/znsyhandao/skills/sleep-health-assistant)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [CHANGELOG.md](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, JSON]

**Output Format:** [Structured JSON-like command responses with human-readable wellness guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-only responses based on user-provided health and wellness inputs; cleanup command clears in-memory session data.]

## Skill Version(s):

1.0.0 (source: server release metadata, config.yaml, skill.py, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
