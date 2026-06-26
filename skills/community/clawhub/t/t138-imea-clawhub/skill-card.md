## Description: <br>
T138 Imea Clawhub provides an Integrated Memory Evolution Action workflow for agents to search local memory, reuse lessons, maintain WAL state, and enforce before-action checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chungvic](https://clawhub.ai/user/chungvic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure local memory tiers, before-action checks, and learning records so agents can consult past task history and reduce repeated errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages persistent local recording and reuse of conversation and task history, with weak privacy and deletion controls. <br>
Mitigation: Install only when persistent local agent memory is intentional; exclude secrets and confidential conversations, and define retention and deletion processes for L1/L2/L3 memory files and SESSION-STATE.md. <br>
Risk: Before-action and heartbeat workflows can run local checks that inspect workspace memory and learning files. <br>
Mitigation: Inspect scripts/memory-check.sh before enabling hooks, and allow indexing only in approved workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chungvic/t138-imea-clawhub) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [Triple memory system configuration](config/triple-memory-system.md) <br>
- [Agent memory certificate](config/agent-memory-certificate.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation with JSON configuration examples and bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a local memory-check shell script and persistent L1/L2/L3 memory file conventions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
