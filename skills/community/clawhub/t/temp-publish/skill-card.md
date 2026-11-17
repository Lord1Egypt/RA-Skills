## Description:

Skill Cortex helps an agent acquire, use, learn from, and clean up short-term Skills when existing installed Skills cannot complete a task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ankwu001](https://clawhub.ai/user/ankwu001)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw agent users can use this skill to let an agent search for, install, execute, learn from, and remove short-term Skills for tasks outside its current capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to install and run other skills on demand, including third-party sources.

Mitigation: Require explicit approval, source verification, and full package inspection before every install and execution.

Risk: The security summary flags the reflex path as allowing high-impact read-only execution with weak opt-out wording.

Mitigation: Keep reflex behavior disabled or edit it to require explicit confirmation, unchanged versions, verified sources, and clear cancellation before execution.

Risk: Delegating work to newly installed skills can expose the user to the installed skill's own behavior and risks.

Mitigation: Review each installed skill's security scan, side effects, requested credentials, and execution plan before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ankwu001/skills/temp-publish)
- [ClawHub](https://clawhub.ai)
- [OpenClaw](https://github.com/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update a local cortex.json memory file and propose skill installation or cleanup actions.]

## Skill Version(s):

0.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
