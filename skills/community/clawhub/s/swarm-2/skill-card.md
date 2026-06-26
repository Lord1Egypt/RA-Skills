## Description: <br>
SWARM: System-Wide Assessment of Risk in Multi-agent systems. 38 agent types, 29 governance levers, 55 scenarios. Study emergent risks, phase transitions, and governance cost paradoxes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsavitt](https://clawhub.ai/user/rsavitt) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, safety researchers, and governance teams use this skill to run and interpret local multi-agent safety simulations, including scenario sweeps, governance levers, phase-transition studies, and API or CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an external Python package and optional extras. <br>
Mitigation: Install only from the expected PyPI package or GitHub repository, consider pinning the package version, and enable extras only when needed. <br>
Risk: The optional development API has no authentication and is intended for localhost use. <br>
Mitigation: Keep the API bound to 127.0.0.1; add authentication, firewall controls, and persistent storage before any production or network exposure. <br>
Risk: Scenario content can accidentally include real secrets, credentials, or personal data. <br>
Mitigation: Use synthetic scenarios and avoid placing API keys, credentials, or personal data in scenario files or API submissions. <br>
Risk: Simulation outputs can be mistaken for ground truth about real systems. <br>
Mitigation: Treat outputs as research artifacts, disclose simulation parameters when publishing, and avoid presenting results as definitive measurements of real deployments. <br>


## Reference(s): <br>
- [SWARM ClawHub release](https://clawhub.ai/rsavitt/swarm-2) <br>
- [SWARM GitHub repository](https://github.com/swarm-ai-safety/swarm) <br>
- [SWARM documentation](https://github.com/swarm-ai-safety/swarm/tree/main/docs) <br>
- [SWARM theoretical foundations](https://github.com/swarm-ai-safety/swarm/tree/main/docs/research/theory.md) <br>
- [SWARM governance guide](https://github.com/swarm-ai-safety/swarm/tree/main/docs/governance.md) <br>
- [SWARM red-teaming guide](https://github.com/swarm-ai-safety/swarm/tree/main/docs/red-teaming.md) <br>
- [SWARM scenario format](https://github.com/swarm-ai-safety/swarm/tree/main/docs/guides/scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python, YAML, bash, and HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local CLI, Python, and localhost API workflows that can export simulation results as JSON or CSV.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter, skill.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
