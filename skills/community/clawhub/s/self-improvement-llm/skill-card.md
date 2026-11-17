## Description:

Autonomous memory and self-learning system for AI agents that logs experience, extracts reusable lessons, manages persistent memory, proposes behavior changes, and verifies whether improvements worked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucetangc](https://clawhub.ai/user/brucetangc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add persistent self-improvement workflows to an AI agent, including learning logs, memory distillation, preference tracking, skill draft generation, and later verification of behavior changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived text can persist into future agent memory and instruction files.

Mitigation: Install only when persistent agent memory is intended, and review generated changes before allowing them to influence future behavior.

Risk: Automatic promotion, dream distillation, and startup hooks can change local workspace behavior without direct prompting.

Mitigation: Disable or manually gate automatic promotion, dream distillation, and the startup hook unless those behaviors are explicitly desired.

Risk: ZIP import and skill approval helpers can introduce untrusted local files.

Mitigation: Use backup import and skill approval helpers only with trusted archives or reviewed drafts, and keep backups before migration or restore operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucetangc/skills/self-improvement-llm)
- [CLI Reference & Detailed Structures](references/cli_ref.md)
- [Reflection Frameworks](references/reflection_frameworks.md)
- [pskoett/self-improving-agent](https://clawhub.ai/pskoett/self-improving-agent)
- [Hermes Agent](https://github.com/NousResearch/hermes-agent)
- [Reflexion](https://arxiv.org/abs/2303.11366)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON memory records, and generated skill or configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local memory, preference, hook-context, and skill draft files when its workflows are run.]

## Skill Version(s):

2.3.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
