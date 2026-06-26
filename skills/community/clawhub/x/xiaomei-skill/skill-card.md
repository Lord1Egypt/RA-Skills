## Description: <br>
Xiaomei Skill provides a local OpenClaw companion agent for emotional companionship, persona simulation, memory-backed conversations, and optional LLM-assisted responses. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[xavier7803](https://clawhub.ai/user/xavier7803) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run a companion subagent that can respond conversationally, maintain persona state, store local memories, and expose status or developer-mode diagnostics. The artifact describes public testing and non-commercial learning use rather than a production commercial release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive local memories, chat history, and logs. <br>
Mitigation: Install only when local storage of companion memories and logs is acceptable, and review how to inspect, disable, or delete those files. <br>
Risk: Privacy, network-use, logging, and packaging disclosures are inconsistent. <br>
Mitigation: Treat local-only claims cautiously, disable external LLM or API mode unless needed, and verify downloaded runtime scripts before running them. <br>
Risk: The release is flagged as suspicious by the authoritative security evidence. <br>
Mitigation: Review the skill before installation and confirm credential handling, network configuration, and logging behavior in the installed environment. <br>


## Reference(s): <br>
- [ClawHub Xiaomei Skill page](https://clawhub.ai/xavier7803/xiaomei-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/xavier7803) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [Artifact support link](https://github.com/xavier7803/xiaomei-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Configuration, Shell commands] <br>
**Output Format:** [Conversational text with command responses and optional structured local logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local persona, memory, chat history, and developer log files when enabled.] <br>

## Skill Version(s): <br>
0.9.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
