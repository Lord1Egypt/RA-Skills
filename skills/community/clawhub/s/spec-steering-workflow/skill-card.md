## Description:

Use a lightweight spec + steering workflow for long, interruptible, multi-phase tasks that need checkpointed progress, recoverable state, and multi-session continuity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whisper1952717](https://clawhub.ai/user/whisper1952717)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create, resume, checkpoint, validate, and archive long-running work through file-based specs and steering files. It is suited to multi-phase tasks that need durable handoffs across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled local script can operate outside its intended workspace folders if given a crafted spec name.

Mitigation: Validate spec IDs, enforce path containment before file operations, and avoid using spec names supplied by untrusted content.

Risk: Implicit invocation may create or resume workflow state when that state change was not intended.

Mitigation: Prefer disabling implicit invocation or requiring confirmation before creating or resuming workflow state.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/whisper1952717/skills/spec-steering-workflow)
- [ClawHub Homepage](https://clawhub.ai/skills?sort=downloads)
- [Workflow Rules](references/workflow-rules.md)
- [Checkpoint Rules](references/checkpoint-rules.md)
- [Recovery Rules](references/recovery-rules.md)
- [Template Contracts](references/template-contracts.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates workspace spec, steering, handoff, task, and metadata files when the bundled CLI is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
