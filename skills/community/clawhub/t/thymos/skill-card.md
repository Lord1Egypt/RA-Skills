## Description: <br>
Background daemon that models an OpenClaw agent's evolving emotional state via neuromodulators, circadian rhythm, social cues, and memory for nuanced responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paperbags1103-hash](https://clawhub.ai/user/paperbags1103-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can use Thymos to add a persistent local emotional-state and relationship-memory layer that shapes an agent's tone and behavioral guidance across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A mutable local prompt field can persistently steer agent behavior before every reply. <br>
Mitigation: Treat emotional_state.json and its prompt_injection field as untrusted input, and limit Thymos guidance to tone and style rather than task, policy, or safety priority. <br>
Risk: The optional daemon changes local state continuously and may add network behavior when proactive Discord messaging is enabled. <br>
Mitigation: Audit the daemon before running it, keep proactive messaging disabled unless explicitly needed, and review any Discord configuration before use. <br>
Risk: Local relationship and emotional memory files may contain user identifiers or message fragments. <br>
Mitigation: Protect the local data directory and periodically delete local state files when retention is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paperbags1103-hash/thymos) <br>
- [Publisher profile](https://clawhub.ai/user/paperbags1103-hash) <br>
- [Usage guide](docs/USAGE.en.md) <br>
- [Security notes](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local JSON file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is applied from local emotional state when present; otherwise the agent skips it and responds normally.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
