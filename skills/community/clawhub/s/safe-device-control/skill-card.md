## Description:

Physical-device control safety gate - never blindly toggle cloud devices; check state, surface risk, require explicit go-ahead before risky actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hohobohan](https://clawhub.ai/user/hohobohan)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and operators use this skill before controlling physical or cloud-connected devices to check current state, classify action risk, surface hazards, request explicit approval for risky actions, and verify outcomes after execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Physical device actions can have real-world effects, including disconnecting a device, requiring physical recovery, or changing persistent state.

Mitigation: Read current device state before action, classify risk, surface likely failure modes, require explicit approval for risky or irreversible actions, and verify state after each command.

Risk: The artifact names a specific approver and environment-specific devices, which may not match a new deployment.

Mitigation: Review and adapt device names, recovery procedures, and the named approver before relying on the skill in another environment.

## Reference(s):

- [Safe Device Control on ClawHub](https://clawhub.ai/hohobohan/skills/safe-device-control)
- [Dreame AP10 Integration MiOT Reference](https://github.com/CodyJon/dreame-ap10-integration)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces safety checklists, risk classifications, approval prompts, and verification guidance before device-control actions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
