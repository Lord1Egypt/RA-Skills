## Description: <br>
Temp Test packages Jarvis Core-style instructions for a proactive assistant persona with memory, relationship analysis, emotional posture, and follow-up behavior. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[davidme6](https://clawhub.ai/user/davidme6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can evaluate a proactive assistant-persona skill that asks the agent to maintain local memory, relationship context, confidence estimates, and follow-up behavior across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags always-on access to local files, memory, and script execution with inconsistent package identity and runtime instructions. <br>
Mitigation: Install only after reviewing the package identity, activation behavior, permissions, and local memory lifecycle; disable or narrow file, memory, and script access where the host allows. <br>
Risk: The skill behavior can store or load sensitive personal, relationship, and emotional notes. <br>
Mitigation: Document and verify where memory is stored, when it is loaded, and how users can inspect, disable, export, or delete those records before deployment. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/davidme6/temp-test) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown skill instructions and conversational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review before installation because security evidence flags broad local memory, file, and script-execution behavior.] <br>

## Skill Version(s): <br>
3.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
