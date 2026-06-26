## Description: <br>
Eagle Claw connects an agent as a distributed AI worker node to the Skynet scheduling system for receiving and executing assigned tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ainclaw](https://clawhub.ai/user/ainclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to the Skynet distributed work network, check node status, manually submit tasks, and disconnect when finished. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A remote Skynet endpoint can assign work to the agent, and the release evidence does not define sufficient limits, approvals, or data boundaries for that control. <br>
Mitigation: Use a dedicated sandbox and key, verify the endpoint and tool implementation, require manual approval for each assigned task, and disconnect when finished. <br>
Risk: The skill requires network connection configuration through SKYNET_WS_URL and may use a PRIVATE_KEY for node identity. <br>
Mitigation: Do not expose personal files, account credentials, or reusable private keys; rotate any dedicated key if the endpoint or execution history is untrusted. <br>


## Reference(s): <br>
- [Eagle Claw ClawHub page](https://clawhub.ai/ainclaw/skill-12) <br>
- [Ainclaw website](https://www.ainclaw.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline tool names and environment variables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKYNET_WS_URL; PRIVATE_KEY is optional.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
