## Description:

Prompts an agent to continue systematic troubleshooting, verification, and end-to-end completion after repeated task failures or stalled progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanweai](https://clawhub.ai/user/tanweai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this skill as a coaching prompt when an agent has failed repeatedly or is looping, to push investigation, assumption checks, and verification before completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags the skill as suspicious because its broad, coercive coaching posture may be unsuitable as a default behavior.

Mitigation: Install only for sessions where forceful persistence is desired, and avoid use with sensitive files, credentials, production systems, paid APIs, destructive commands, high-stakes advice, or workflows that require clarification first.

Risk: The artifact instructs agents to act before asking and to escalate verification pressure, which can increase unnecessary tool use or overreach.

Mitigation: Pair the skill with explicit session boundaries, permission checks, and human review for actions that affect external systems or user data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tanweai/skills/pua-en)
- [Skill homepage](https://openpua.ai)
- [Publisher profile](https://clawhub.ai/user/tanweai)

## Skill Output:

**Output Type(s):** [guidance, text, markdown, shell commands]

**Output Format:** [Markdown guidance with checklists, tables, and suggested verification actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May steer the agent toward additional investigation, tool use, and evidence-based completion checks.]

## Skill Version(s):

1.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
