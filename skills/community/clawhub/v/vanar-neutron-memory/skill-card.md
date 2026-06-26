## Description: <br>
Save and recall agent memory with semantic search. Context that persists across every session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[naeemmaliki036](https://clawhub.ai/user/naeemmaliki036) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to save selected context to a hosted memory service and later retrieve semantically relevant memories across sessions. Optional hooks can automatically capture and recall conversation context when explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved memories, search queries, and optionally conversation turns are sent to a hosted remote memory service. <br>
Mitigation: Use the skill only for data suitable for that service, keep auto-capture and auto-recall disabled unless needed, and avoid storing secrets, regulated data, or confidential business content. <br>
Risk: The skill requires an API key for hosted memory operations. <br>
Mitigation: Provide the key through the documented environment variable or credentials file and rotate it if it is exposed. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/naeemmaliki036/vanar-neutron-memory) <br>
- [Setup guide](SETUP.md) <br>
- [OpenClaw dashboard and API keys](https://openclaw.vanarchain.com/) <br>
- [OpenClaw signup](https://openclaw.vanarchain.com/signup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and an API key; remote save and search operations send selected text or search queries over HTTPS.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
