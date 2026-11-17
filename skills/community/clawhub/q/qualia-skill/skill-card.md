## Description:

Fine-tune robot foundation models on Qualia cloud GPUs, including VLA, ACT, SmolVLA, pi0, pi0.5, GR00T N1.5, and SARM reward-model workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fabbe1999](https://clawhub.ai/user/fabbe1999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, robotics engineers, and agent users use this skill to launch, monitor, tune, cancel, and troubleshoot Qualia cloud fine-tuning jobs for robot foundation models using LeRobot-format HuggingFace datasets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses QUALIA_API_KEY for authenticated cloud API calls, so exposed keys could allow unauthorized access to credits, projects, or jobs.

Mitigation: Store QUALIA_API_KEY in managed secrets or agent environment configuration, and avoid placing the key in prompts, logs, screenshots, or source files.

Risk: Training launches can consume Qualia credits and start remote GPU jobs.

Mitigation: Estimate cost with the instances and credits commands, then require explicit user approval before launching paid training.

Risk: Job cancellation and project deletion can interrupt or remove user work.

Mitigation: Confirm the exact job_id or project_id with the user before running cancel or project-delete commands.

Risk: Dataset IDs, job metadata, camera mappings, and hyperparameters are sent to Qualia cloud services.

Mitigation: Use the skill only with datasets and training parameters the user is comfortable sharing with Qualia.

## Reference(s):

- [Qualia Homepage](https://qualiastudios.dev)
- [Qualia App](https://app.qualiastudios.dev)
- [Qualia LLM Context](https://docs.qualiastudios.dev/llms.txt)
- [Qualia API Reference](https://dev-docs.qualiastudios.dev/api/reference)
- [Qualia SDK Overview](https://docs.qualiastudios.dev/sdk/overview/)
- [Qualia Guides](https://docs.qualiastudios.dev/global/guides/)
- [ClawHub Skill Page](https://clawhub.ai/fabbe1999/skills/qualia-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI supports a global --json flag and stable exit codes for agent-driven workflows.]

## Skill Version(s):

2.1.1 (source: evidence.release.version, SKILL.md frontmatter, CHANGELOG.md released 2026-06-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
