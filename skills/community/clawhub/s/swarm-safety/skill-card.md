## Description:

SWARM: System-Wide Assessment of Risk in Multi-agent systems. Simulate multi-agent dynamics with 38 agent types and 29 governance levers to study emergent risks, phase transitions, and governance cost trade-offs using soft probabilistic labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsavitt](https://clawhub.ai/user/rsavitt)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and safety reviewers use this skill to install and run SWARM simulations, scenario sweeps, governance experiments, and local API workflows for multi-agent risk analysis. Outputs should be treated as simulation artifacts rather than ground truth about real deployed systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional development API has no authentication and should not be exposed to untrusted networks.

Mitigation: Run it on localhost, avoid binding it to public interfaces, and add authentication plus durable storage before any production deployment.

Risk: Scenarios or prompts may contain real secrets, credentials, or personal data.

Mitigation: Use synthetic or scrubbed inputs and do not submit real API keys, credentials, or PII in scenarios.

Risk: Simulation outputs can be overinterpreted as real-world safety conclusions.

Mitigation: Treat results as research artifacts, disclose simulation parameters, and validate findings before using them for operational decisions.

Risk: Unpinned package installation can reduce reproducibility.

Mitigation: Install in a dedicated virtual environment or container and use a reviewed pinned package version or commit when reproducible runs are required.

## Reference(s):

- [SWARM Safety ClawHub page](https://clawhub.ai/rsavitt/skills/swarm-safety)
- [Publisher profile](https://clawhub.ai/user/rsavitt)
- [SWARM repository](https://github.com/swarm-ai-safety/swarm)
- [SWARM documentation](https://github.com/swarm-ai-safety/swarm/tree/main/docs)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with Python, YAML, JSON, curl, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local simulation runs, scenario authoring, governance configuration, metric interpretation, and optional localhost API usage.]

## Skill Version(s):

1.7.1 (source: server release evidence; artifact frontmatter and skill.json list 1.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
