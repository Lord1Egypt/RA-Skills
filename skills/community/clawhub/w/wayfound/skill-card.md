## Description:

Lightweight self-supervision that piggybacks on an existing memory system by adding a SOUL.md rubric and a daily review cron job.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cburnette](https://clawhub.ai/user/cburnette)

### License/Terms of Use:


## Use Case:

External users and developers use Wayfound to add lightweight daily self-review to an OpenClaw agent, record findings in memory, and surface recurring quality or behavior issues for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sets up a persistent daily self-review agent through a cron job.

Mitigation: Require explicit approval before enabling the cron job, review the exact job behavior, and document how to disable or delete it.

Risk: Review results can lead to changes in long-term memory or identity files such as MEMORY.md and SOUL.md.

Mitigation: Require explicit approval before applying changes to MEMORY.md or SOUL.md from review results.

Risk: External alerting or Wayfound Enterprise use may involve additional data sharing.

Mitigation: Treat those features as separate integrations requiring their own consent and privacy review.

## Reference(s):

- [Wayfound homepage](https://wayfound.ai)
- [Wayfound on ClawHub](https://clawhub.ai/cburnette/skills/wayfound)
- [Publisher profile](https://clawhub.ai/user/cburnette)
- [Rubric examples](references/rubric-examples.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily review output is intended to be short markdown, about 10-15 lines.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
