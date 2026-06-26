## Description: <br>
Local memory search for OpenClaw agents that runs a lightweight Node.js server to index local memory files and expose keyword search through a web UI and API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wrentheai](https://clawhub.ai/user/wrentheai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agent users use this skill to search past local memory, session history, daily logs, decisions, and resolved issues without relying on external services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive local agent memory may be exposed through an unauthenticated HTTP server. <br>
Mitigation: Use the skill only when local memory search is intended, bind the listener to 127.0.0.1 where possible, and add access controls before exposing it beyond the local machine. <br>
Risk: The server can be installed as a persistent login service. <br>
Mitigation: Avoid loading the LaunchAgent unless persistent startup is intended, and review or remove the login item when the server is no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and a local JSON HTTP API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can start or check a local server and return search results from local memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
