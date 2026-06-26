## Description: <br>
Connects a running agent runtime to XMTP messaging so people can DM it, preserve conversation context, and receive responses through a persistent bridge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saulmc](https://clawhub.ai/user/saulmc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to make an existing agent reachable over XMTP for ongoing two-way conversations. It provides bridge setup guidance, identity registration steps, and backend routing patterns for owner and public sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A persistent XMTP bridge may route messages from strangers into a local agent that has tools, memory, or file access. <br>
Mitigation: Run the bridge in a contained environment and use a separate no-tools/no-files public backend instead of relying only on a prompt prefix. <br>
Risk: Incorrect owner identification can give the wrong sender full agent capabilities. <br>
Mitigation: Verify the owner inbox ID before starting the bridge and keep trusted-user allowlists explicit and minimal. <br>
Risk: XMTP wallet and encryption keys can grant control over the messaging identity if exposed. <br>
Mitigation: Protect the generated XMTP key material and avoid sharing or committing the local XMTP environment file. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/saulmc/xmtp-agents) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with bash, JSON, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup commands, bridge script templates, public prompt guidance, and backend-specific routing examples.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
