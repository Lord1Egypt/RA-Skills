## Description:

Skill Cortex helps an OpenClaw agent find, install, use, and remove short-term skills from ClawHub or GitHub while learning routing patterns for future tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ankwu001](https://clawhub.ai/user/ankwu001)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill when an OpenClaw agent lacks a needed capability and should search for, install, execute, and clean up an appropriate skill with user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can acquire and run other skills on demand, including broad third-party candidates.

Mitigation: Use trusted ClawHub sources where possible, avoid unreviewed GitHub candidates, and require explicit user approval before each install or candidate switch.

Risk: Reflex execution can reduce review for learned read-only workflows.

Mitigation: Do not allow reflex mode for skills that read credentials, local sensitive data, or use the network; require normal review when versions change or failures occur.

Risk: Persistent routing memory can affect future skill choices and may need cleanup.

Mitigation: Periodically inspect or reset ~/.openclaw/skill-cortex/cortex.json and rely on entity filtering for stored signal words.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ankwu001/skills/skill-cortex-ank)
- [Publisher Profile](https://clawhub.ai/user/ankwu001)
- [OpenClaw](https://github.com/openclaw)
- [ClawHub](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the clawhub CLI and may update local short-term routing memory.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
