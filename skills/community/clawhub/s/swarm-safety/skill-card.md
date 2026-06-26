## Description: <br>
SWARM: System-Wide Assessment of Risk in Multi-agent systems. Simulate multi-agent dynamics with 38 agent types and 29 governance levers to study emergent risks, phase transitions, and governance cost tradeoffs. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[rsavitt](https://clawhub.ai/user/rsavitt) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, safety researchers, and governance teams use this skill to install and run SWARM simulations, author scenarios, compare agent populations and governance levers, and interpret multi-agent risk metrics as research artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scenario files could contain real API keys, credentials, or personal data. <br>
Mitigation: Do not put real secrets or PII into scenario files; use synthetic or redacted inputs. <br>
Risk: The unauthenticated development API could be exposed if bound beyond localhost. <br>
Mitigation: Keep the API bound to 127.0.0.1 unless authentication, firewalling, and production storage are added. <br>
Risk: Simulation outputs could be mistaken for real-world ground truth. <br>
Mitigation: Treat results as research artifacts and disclose scenario parameters when publishing or sharing findings. <br>
Risk: Installing and running the upstream package executes third-party code. <br>
Mitigation: Install in a virtual environment or container and review the upstream package or source when higher assurance is needed. <br>


## Reference(s): <br>
- [SWARM Safety on ClawHub](https://clawhub.ai/rsavitt/swarm-safety) <br>
- [SWARM project homepage](https://github.com/swarm-ai-safety/swarm) <br>
- [SWARM documentation](https://github.com/swarm-ai-safety/swarm/tree/main/docs) <br>
- [Skill metadata](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python, YAML, bash, and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May refer to local simulation outputs such as JSON or CSV exports when the user runs SWARM commands.] <br>

## Skill Version(s): <br>
1.7.1 (source: server release metadata; artifact frontmatter reports 1.7.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
