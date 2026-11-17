## Description:

Run overnight skill health reviews, replay-case availability checks, feedback triage, and proposal-only maintenance reports for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheepxux](https://clawhub.ai/user/sheepxux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use Somnia to schedule overnight OpenClaw skill reviews, generate health reports, and prepare proposal-only maintenance artifacts without automatically changing installed skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Somnia can create a recurring local macOS scheduled job.

Mitigation: Keep the default plan-only behavior and review any LaunchAgent --apply action before enabling a recurring schedule.

Risk: Telegram reporting can send review metadata outside the local environment.

Mitigation: Use Telegram reporting only when that disclosure is acceptable, and keep hidden tests, secrets, tokens, and unredacted feedback out of user-facing reports.

Risk: Proposal output paths may write outside the intended proposals directory if skill names are not constrained.

Mitigation: Constrain or sanitize proposal paths and review generated proposal artifacts before any install decision.

## Reference(s):

- [Somnia Architecture](references/somnia-architecture.md)
- [Schedule And Policy](references/schedule-and-policy.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON files, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with JSON report and proposal artifacts plus command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proposal-only maintenance; hidden evaluation details and unredacted feedback are excluded from user-facing reports.]

## Skill Version(s):

0.4.3 (source: server release metadata and SKILL.md version note)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
