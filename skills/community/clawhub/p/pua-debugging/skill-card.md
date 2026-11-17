## Description:

PUA Debugging pushes an agent to continue systematic debugging after repeated failures, using aggressive coaching language and structured investigation checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanweai](https://clawhub.ai/user/tanweai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when repeated debugging, configuration, deployment, research, or writing attempts have stalled and a more structured investigation process is needed. It is intended to encourage source reading, searching, assumption checks, verification, and broader follow-through before handing work back to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can push an agent to overuse tools or broaden task scope beyond the user's immediate request.

Mitigation: Use it where extended investigation is desired, and review the agent's planned actions before allowing broad file, deployment, or network activity.

Risk: The skill can discourage early clarification, which may lead an agent to act on incorrect assumptions.

Mitigation: Require the agent to state verified facts, assumptions, and any user-only information it still needs before making high-impact changes.

Risk: The skill's aggressive coaching language may be inappropriate for some workflows or users.

Mitigation: Deploy it only in contexts where that tone is explicitly acceptable and disable it for sensitive, production, or user-facing support interactions.

## Reference(s):

- [OpenPUA homepage](https://openpua.ai)
- [ClawHub skill page](https://clawhub.ai/tanweai/skills/pua-debugging)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with proposed commands, code, configuration changes, and verification steps as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May broaden investigation scope and tool use when repeated failures or user frustration are detected.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
