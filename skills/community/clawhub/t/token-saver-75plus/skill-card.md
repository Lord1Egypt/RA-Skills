## Description: <br>
Automatically classifies requests to optimize cost by routing to the cheapest capable model and applies maximum output compression for 75%+ token savings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariovallereyes](https://clawhub.ai/user/mariovallereyes) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and developers use this always-on behavioral protocol to classify requests, compress responses, gate tool use, and route work to cheaper capable models while preserving escalation paths for complex tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages persistent token-compression and model-routing behavior, including sending full task context to spawned model agents. <br>
Mitigation: Install only when this behavior is intended, require confirmation before spawning agents on sensitive work, and share only the minimum context needed. <br>
Risk: Model routing can affect provider cost, privacy, and tool access boundaries. <br>
Mitigation: Check model and provider cost and privacy implications before use, and limit spawned-agent tools according to local policy. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mariovallereyes/token-saver-75plus) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with routing tables, command examples, and concise response templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Applies tiered output budgets, tool gating, and optional measurement annotations when testing is requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
