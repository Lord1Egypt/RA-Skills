## Description:

QRQC Quick Response helps frontline manufacturing and quality teams put same-day anomalies on a QRQC response board, assign ownership, and track shift-level closure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing supervisors, team leads, and quality engineers use this skill during QRQC stand-up response meetings to capture production or quality anomalies, record containment actions, assign a single owner, and track same-shift closure or escalation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated QRQC board contents may be inaccurate or incomplete if source issue details are missing.

Mitigation: Review generated board contents for accuracy and keep missing fields marked as 待补充 until confirmed.

Risk: Same-day report names can collide when multiple QRQC boards are generated.

Mitigation: Ask the agent to write outputs to a dedicated folder or unique filename when same-day report collisions matter.

## Reference(s):

- [Server-resolved source repository](https://github.com/duding-engicool/skill-qrqc-quick-response)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-qrqc-quick-response)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Plain text and Markdown QRQC response boards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Missing fields are marked as 待补充; outputs are intended for meeting review, printing, or downstream system import.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
