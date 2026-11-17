## Description:

SWARM: System-Wide Assessment of Risk in Multi-agent systems. 38 agent types, 29 governance levers, 55 scenarios. Study emergent risks, phase transitions, and governance cost paradoxes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsavitt](https://clawhub.ai/user/rsavitt)

### License/Terms of Use:

MIT

## Use Case:

Developers, safety researchers, and governance reviewers use this skill to simulate multi-agent AI dynamics, study emergent risk patterns, and evaluate governance levers with CLI, Python, and optional localhost API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional development API has no authentication and could expose simulation functions if bound beyond localhost.

Mitigation: Keep the API on localhost, do not expose it to untrusted networks, and add authentication plus a proper database before production deployment.

Risk: Scenarios may accidentally include real secrets, credentials, or personal data.

Mitigation: Use synthetic scenario data only and review inputs before running or sharing simulations.

Risk: Simulation results can be mistaken for ground truth about real multi-agent systems.

Mitigation: Treat outputs as research artifacts, disclose parameters when publishing, and validate conclusions with independent review.

Risk: Local package installation and optional extras can introduce ordinary dependency and reproducibility risks.

Mitigation: Install in a virtual environment or container and pin dependency versions when reproducibility matters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rsavitt/skills/swarm-2)
- [SWARM Repository](https://github.com/swarm-ai-safety/swarm)
- [SWARM Documentation](https://github.com/swarm-ai-safety/swarm/tree/main/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python, YAML, shell, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local simulation setup, scenario authoring, metric interpretation, and optional localhost API usage.]

## Skill Version(s):

1.5.0 (source: frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
