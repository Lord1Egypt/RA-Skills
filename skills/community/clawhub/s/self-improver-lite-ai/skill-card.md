## Description:

Runs lightweight self-audits of OpenClaw behavior, finds repeated failures, proposes safe config/process improvements, and tracks what changed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utromaya-code](https://clawhub.ai/user/utromaya-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit OpenClaw reliability after incidents, repeated errors, configuration changes, silent-bot periods, rate-limit spikes, or scheduled weekly maintenance. It helps group failures, identify likely root causes, propose minimal reversible fixes, and track resulting changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic service restarts or persistent configuration changes could affect production OpenClaw availability or behavior.

Mitigation: Require the agent to show the exact restart, cleanup, or configuration change before applying it, and keep a rollback path such as backing up old configuration before edits.

Risk: Operational reports could expose secrets or sensitive runtime details.

Mitigation: Keep secrets out of reports and review collected logs before sharing audit summaries.

Risk: Multiple changes in one cycle can make it hard to determine which change affected reliability.

Mitigation: Prefer one change per cycle and record the change, measured impact, rollback path, and next action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utromaya-code/skills/self-improver-lite-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include weekly audit summaries, proposed reversible fixes, rollback notes, and approval requests for higher-impact actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
