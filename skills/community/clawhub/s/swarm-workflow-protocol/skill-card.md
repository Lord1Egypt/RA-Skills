## Description: <br>
Multi-agent orchestration protocol for the 0x-wzw swarm. Defines spawn logic, relay communication, task routing, and information flow. Agents drive decisions; humans spar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x-wzw](https://clawhub.ai/user/0x-wzw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to plan multi-agent work, decide when spawning is worth the overhead, route tasks, and standardize relay handoffs and logging for the 0x-wzw swarm. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents a reusable local relay token and relay endpoints. <br>
Mitigation: Replace the documented token with a unique secret, keep the relay in a trusted local environment, and restrict access to approved agents and sources. <br>
Risk: The workflow encourages broad autonomous execution and continuous relay logging. <br>
Mitigation: Define approval boundaries, redaction rules, log retention, and limits on what agents may relay or persist before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0x-wzw/swarm-workflow-protocol) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with relay endpoint examples and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes relay message formats, local endpoint examples, and audit log paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
