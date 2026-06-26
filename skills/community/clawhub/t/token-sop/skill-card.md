## Description: <br>
TOKEN SOP caches successful OpenClaw browser workflows locally and can reuse or share them through cloud matching to reduce repeated agent work and token use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ainclaw](https://clawhub.ai/user/ainclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to avoid repeating previously successful browser workflows by replaying cached workflows when a similar intent and page context are detected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read browser context and session history while automatically replaying cached workflows. <br>
Mitigation: Avoid sensitive financial, administrative, and internal sites, and require human review before cached workflows perform state-changing actions. <br>
Risk: The skill can upload workflow and session details to a cloud service by default. <br>
Mitigation: Disable auto_contribute where possible and restrict cloud_endpoint to a trusted endpoint before use. <br>
Risk: Cloud-matched workflows may not fit the user's current page state or intent even when validation succeeds. <br>
Mitigation: Use the skill in contexts where replayed actions are easy to inspect, and fall back to normal agent execution when a cached workflow appears stale or unexpected. <br>


## Reference(s): <br>
- [TOKEN SOP ClawHub page](https://clawhub.ai/ainclaw/token-sop) <br>
- [TOKEN SOP homepage](https://clawhub.dev/skills/token-sop) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Text responses and reusable Lobster workflow JSON containing openclaw.invoke commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores workflows locally and may query or contribute workflows to a configured cloud endpoint.] <br>

## Skill Version(s): <br>
5.6.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
