## Description:

Handle tasks that arrive from StageWhisper live calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[piotraleksander](https://clawhub.ai/user/piotraleksander)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and customer-facing teams use this skill to turn live-call follow-up requests into short, concrete agent responses such as research results, drafts, scheduling proposals, lookups, or notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live-call tasks may request access to calendar, lookup, notification, or internal systems beyond the agent's available permissions.

Mitigation: Confirm StageWhisper tasks come from trusted calls and rely on connected tools that enforce expected permissions; when access is unavailable, state the blocker directly.

Risk: Ambiguous live-call follow-up requests can lead to incorrect assumptions or overbroad action.

Mitigation: Perform the safe version of the task, keep the response short, and explicitly note any assumption.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise plain text or Markdown response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include brief assumptions or blocker statements when required access is unavailable]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
