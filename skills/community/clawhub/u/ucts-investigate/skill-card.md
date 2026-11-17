## Description:

Guides agents through systematic, hypothesis-driven root cause debugging with explicit investigation steps, falsifiable hypotheses, and reassessment after repeated failed fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muthukumaran-k-1](https://clawhub.ai/user/muthukumaran-k-1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to structure debugging conversations: reproduce the issue, rank falsifiable hypotheses, trace data flow, run minimal tests, and reassess after three failed fix attempts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can advise escalation into Claude Code when code inspection, test execution, or edits are needed, while the short description says no Claude Code session is needed.

Mitigation: Treat escalation as conditional: remain in chat for reasoning-only debugging and move to a code session only when hands-on repository work is required.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown guidance with occasional inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code, credential access, persistence, or hidden data movement is identified in the security evidence.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
