## Description:

Evaluate external skills before installation and decide whether to install, reject, or absorb only the useful ideas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g-hanasq](https://clawhub.ai/user/g-hanasq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to review external ClawHub or GitHub skills before installation, classify their risk and fit, and choose whether to install, reject, postpone, or absorb ideas only.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to promote ideas from an untrusted skill into persistent workflow or memory files.

Mitigation: Require explicit approval, exact diffs, clear destination paths, and rewritten notes before any absorb-ideas action.

Risk: The skill provides workflow guidance rather than executable validation, so installation readiness can remain uncertain after static review alone.

Mitigation: Treat static review as preliminary and require main-agent dynamic validation before calling an external skill fully usable.

## Reference(s):

- [Skill Intake Checklist](references/checklist.md)
- [ClawHub Skill Shell listing](https://clawhub.ai/g-hanasq/skills/skill-shell)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review report with recommendation labels and risk classification]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Decision-oriented output; may identify static review findings, required dynamic validation, environment sensitivity, risks, and fit with the current workflow.]

## Skill Version(s):

0.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
