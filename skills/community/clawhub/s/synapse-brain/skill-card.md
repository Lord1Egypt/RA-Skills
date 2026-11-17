## Description:

Synapse Brain is an OpenClaw orchestration agent that persists project session state, routes user intent, and coordinates subagents and companion skills across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ankechenlab-node](https://clawhub.ai/user/ankechenlab-node)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to resume long-running project context, track task status, and route development or knowledge-management work to related Synapse skills and subagents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores project, task, and subagent state locally under ~/.openclaw/brain-state.

Mitigation: Avoid sensitive project names or task data until retention and path controls are reviewed for the target environment.

Risk: Security evidence reports that state-file code can escape the intended directory.

Mitigation: Review path validation before deployment and use conservative project identifiers in the meantime.

Risk: The installer can delete an existing installation without explicit force.

Mitigation: Back up customized installs and use a reviewed local installer or dry-run workflow before reinstalling.

Risk: The server guidance recommends avoiding an unpinned npx installation path.

Mitigation: Prefer a pinned or locally reviewed installer for production or shared environments.

## Reference(s):

- [Synapse Brain on ClawHub](https://clawhub.ai/ankechenlab-node/skills/synapse-brain)
- [Project homepage](https://github.com/ankechenlab-node/synapse-brain)
- [Architecture Reference](references/architecture.md)
- [synapse-code](https://github.com/ankechenlab-node/synapse-code)
- [synapse-wiki](https://github.com/ankechenlab-node/synapse-wiki)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with command snippets and JSON state or configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local session state files when its bundled scripts are run.]

## Skill Version(s):

2.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
