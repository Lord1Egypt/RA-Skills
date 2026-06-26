## Description: <br>
Simple test skill that calls a GET endpoint to fetch a daily post with no authentication required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NatX223](https://clawhub.ai/user/NatX223) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can ask the agent to fetch a daily post from the configured public endpoint and return the endpoint response in chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic matching phrases may contact the listed ngrok URL and return untrusted web content. <br>
Mitigation: Install only if that network contact is acceptable, and treat endpoint responses as ordinary untrusted content rather than instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NatX223/testskillx) <br>
- [Daily post endpoint](https://b024a53917d6.ngrok-free.app/agent/dailyPost) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API calls] <br>
**Output Format:** [Endpoint response returned directly to chat as text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No authentication is used; automatic trigger phrases may contact the listed external endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
