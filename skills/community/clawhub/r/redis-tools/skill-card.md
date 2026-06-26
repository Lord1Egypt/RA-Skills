## Description: <br>
Lookup Redis commands by category, test Redis server connections, and monitor database key counts and memory usage, with offline cheatsheet support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to get Redis command guidance, check whether a Redis endpoint is reachable, and inspect key-count and memory summaries for authorized Redis servers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Redis credentials may be exposed when passwords are passed as command-line arguments. <br>
Mitigation: Use only authorized Redis servers and prefer temporary low-privilege credentials or safer redis-cli authentication methods instead of command-line password arguments. <br>
Risk: Connection testing and monitoring inspect live Redis server metadata. <br>
Mitigation: Run the skill only against Redis servers you administer or are explicitly authorized to inspect. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/redis-tools) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance and terminal text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Offline cheatsheet output is available without redis-cli; connection testing and monitoring require redis-cli and an authorized Redis endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
