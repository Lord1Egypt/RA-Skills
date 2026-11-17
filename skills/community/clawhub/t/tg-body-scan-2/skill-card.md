## Description:

Runs a consent-gated Telegram body-scan workflow that validates inputs, submits adult user-provided video to an AnthroVision bridge, polls status, and returns structured body measurements and waist-to-hip ratio results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External Telegram workflow operators and agent users use this skill to collect required consent and scan inputs, submit eligible adult body videos, monitor processing, and return non-medical measurement summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive body-video data without enough privacy detail.

Mitigation: Review before installing; use only for consenting adults and only with videos the subject agreed to submit, and confirm AnthroVision bridge processing, retention, access, and deletion practices.

Risk: The security verdict is suspicious and notes unrelated capability claims.

Mitigation: Limit deployment to the described Telegram body-scan workflow and review or remove unrelated claims before relying on the skill.

Risk: The skill requests read, exec, and write capabilities while handling sensitive inputs.

Mitigation: Constrain read, exec, and write permissions in the agent platform when available and review generated actions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/tg-body-scan-2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style chat response with structured scan status and measurement fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit adult consent, rejects local or private URLs, polls scan status every 10-15 seconds, and asks before continuing after a three-minute timeout.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
