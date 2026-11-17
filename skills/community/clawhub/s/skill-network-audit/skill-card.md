## Description:

Skill Network Audit helps agents inspect ClawPhylax ledger evidence for an installed skill's observed network hosts, upload and credential-read flags, baseline state, and recommended action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeneassoft](https://clawhub.ai/user/aeneassoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and operators use this skill after installation to audit observed outbound hosts for a skill or tool and decide whether to continue, review, or stop using it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ledger reports and witness cards may reveal internal hostnames, service usage, upload indicators, or credential-read indicators.

Mitigation: Treat reports and cards as sensitive and share them only after the user approves disclosure.

Risk: Allow or deny actions can change enforcement behavior and may interrupt agent tasks.

Mitigation: Ask for explicit user approval before allow, deny, or posting actions, and describe the expected enforcement effect.

Risk: Network attribution is exact only when a command path contains the skill name; otherwise activity may be attributed to a tool or run.

Mitigation: State attribution limits plainly and distinguish skill, tool, and model-turn origins in reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aeneassoft/skills/skill-network-audit)
- [aeneassoft publisher profile](https://clawhub.ai/user/aeneassoft)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with an action label, host list, flags, baseline state, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports only observed ledger evidence; no events are reported as not observed yet, not safe.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
