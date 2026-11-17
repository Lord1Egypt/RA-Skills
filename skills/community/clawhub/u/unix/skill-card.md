## Description:

Unix provides a six-stage engineering workflow for rigorous requirement clarification, first-principles analysis, build-versus-buy decisions, scoped implementation, adversarial review, and concise delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taotao52](https://clawhub.ai/user/taotao52)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to slow down ambiguous requests, confirm the real goal, choose a minimal solution, implement only the agreed scope, and review the result before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate broadly for engineering requests and may slow direct implementation by requiring clarification first.

Mitigation: Tell the agent to take a direct path or skip early analysis phases when the scope is already clear.

Risk: The workflow shapes agent behavior through prompt instructions, so incorrect scoping or review outputs could affect downstream code or guidance.

Mitigation: Review the proposed scope and final output before applying code, shell commands, or configuration changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taotao52/skills/unix)
- [Publisher profile](https://clawhub.ai/user/taotao52)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with tables, scoped implementation notes, code or shell snippets when needed, and concise final delivery sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable files are bundled; behavior is prompt-driven and may include clarification questions before implementation.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
