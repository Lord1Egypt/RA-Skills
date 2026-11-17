## Description:

Helps an agent avoid premature conclusions by requiring proactive troubleshooting, verification, and evidence before completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to make an agent persist through troubleshooting, gather evidence, verify fixes, and report remaining uncertainty only after major paths have been checked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill pressures an agent to act before asking, which can encourage overreach on sensitive or irreversible operations.

Mitigation: Keep higher-priority policies that require confirmation before destructive changes, credential use, network-affecting actions, public posting, purchases, or broad system modifications.

Risk: A forceful troubleshooting style can push an agent to continue when escalation or clarification is appropriate.

Mitigation: Use the skill with task-specific safety boundaries and require evidence-based status reports when progress stalls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlark/skills/self-apply-pressure)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, Shell commands]

**Output Format:** [Markdown text with verification evidence, command output summaries, or structured failure reports when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Emphasizes objective verification before completion and explicit reporting of unresolved paths.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
