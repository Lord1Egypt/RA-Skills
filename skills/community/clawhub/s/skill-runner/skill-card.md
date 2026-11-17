## Description:

Runs another local OpenClaw skill named in an agentTurn message so scheduled or indirect calls can invoke that skill with the current context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xpneuma](https://clawhub.ai/user/xpneuma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to trigger a named OpenClaw skill from scheduled or indirect agentTurn messages. It is intended for controlled automation where permitted target skills and caller authorization are managed externally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted message could cause the runner to load unintended local skill code with the runner's privileges.

Mitigation: Deploy only with an allowlist of permitted skill names, strict path validation, caller authorization, and a restricted delegated context.

Risk: Delegated execution can expose tools and session context to the target skill.

Mitigation: Run it in a tightly controlled isolated agent and limit the delegated context to the minimum capabilities required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xpneuma/skills/skill-runner)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Structured status object and logs from the delegated skill execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on the delegated skill and may include completion status, target skill name, result payload, or error reason.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
