## Description:

Insert breakpoint self-critique before branching work, after user friction, and at risky handoffs so agents catch errors early.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to insert lightweight self-critique at workflow breakpoints before a weak assumption spreads into plans, edits, handoffs, or final recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local critique memory could accumulate details that are not needed for future breakpoint decisions.

Mitigation: Keep only reusable trigger lessons, critique depth preferences, and breakpoint prompts; avoid storing private user details or long postmortems.

Risk: Optional SOUL or AGENTS integration can change workspace steering behavior.

Mitigation: Review the proposed snippets and approve workspace edits only when this critique workflow should be added to that workspace.

Risk: Overusing deep critique can interrupt routine work and reduce momentum.

Mitigation: Use the lightest critique level that can catch the likely error, and reserve deep critique for high-stakes, novel, or failure-prone work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/self-criticism)
- [Skill homepage](https://clawic.com/skills/self-criticism)
- [Setup guide](setup.md)
- [Memory template](memory-template.md)
- [Trigger families](triggers.md)
- [Critique depth levels](levels.md)
- [Memory routing](routing.md)
- [Boundaries and anti-noise rules](boundaries.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local self-critique memory files under ~/self-criticism/ when the user approves setup.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
