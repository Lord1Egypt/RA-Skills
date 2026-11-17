## Description: <br>
Provides an end-to-end encrypted decentralized memory system for AI agents, with native retrieval and explicit fact recording across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to add opt-in persistent memory to compatible AI agents. It guides status checks, browser-based pairing, memory search, and explicit user-authorized fact recording while keeping recovery phrases out of agent context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates local credential material at ~/.total-recall-ai/credentials.json during pairing. <br>
Mitigation: Protect the credential file, avoid exposing it to agent context, and remove or rotate credentials if the machine is shared or compromised. <br>
Risk: A 12-word recovery phrase can compromise encrypted memories if pasted into chat or exposed to tools. <br>
Mitigation: Never ask for, echo, or pass the recovery phrase through the agent; if it is exposed, treat it as compromised and re-pair with new credentials. <br>
Risk: Encrypted memories are stored on a decentralized network for persistence. <br>
Mitigation: Install only when persistent decentralized memory is desired, and record memories only after explicit user instruction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/total-recall-ai-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an agent with tool-use and exec capability; memory operations depend on memory-cli, Node.js 14+, curl, and user pairing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
