## Description:

TriCore Architecture is a deterministic, code-first three-layer memory and cognitive framework for low-resource servers and agents, including the memctl engine, policy constraints, and cognitive tools for planning, ReAct reasoning, and self-evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bertonhan](https://clawhub.ai/user/bertonhan)

### License/Terms of Use:


## Use Case:

Developers and agent operators use TriCore to install a workspace-wide memory and state framework for OpenClaw agents. It routes planning, task state, and knowledge capture through memctl.py and optionally deploys bundled planning, ReAct, and self-evolution skill templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TriCore can persistently change workspace-wide agent policy, memory handling, and compaction behavior.

Mitigation: Review the POLICY.md changes, save the existing OpenClaw compaction prompt, and back up MEMORY.md before running install.sh.

Risk: The self-evolution component can lead agents toward code, skill, and configuration edits.

Mitigation: Enable self-evolution only when human review is required for proposed edits and runtime write permissions are intentionally granted.

Risk: Legacy memory migration may move an existing large MEMORY.md into an archive and replace it with a minimal template.

Mitigation: Back up MEMORY.md and inspect any archived legacy memory before redistributing facts, decisions, and playbooks through memctl.py.

## Reference(s):

- [TriCore skill page](https://clawhub.ai/bertonhan/skills/tricore)
- [TriCore repository declared by the skill](https://github.com/bertonhan/tricore)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or recommend workspace policy, memory, skill, and configuration changes when installed or applied.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
