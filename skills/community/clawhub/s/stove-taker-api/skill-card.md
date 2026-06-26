## Description: <br>
Uses the Stove Protocol Taker API to validate, lock, unlock, fill, reject, and query taker-side orders and fill records with API key authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zschen211](https://clawhub.ai/user/zschen211) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, brokers, and custodian institutions use this skill to operate Stove Protocol taker workflows, including order validation, locking, unlocking, filling, rejection, order queries, fill queries, and WebSocket event interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform live order actions with production credentials, including lock, unlock, fill, reject, and cancellation-result workflows. <br>
Mitigation: Use test credentials first, require explicit user approval before live state-changing actions, and prefer least-privilege production API keys. <br>
Risk: API keys may be exposed if real credentials are passed in command lines, logs, transcripts, or WebSocket URLs. <br>
Mitigation: Use secret handling where available, avoid printing full credentials, and redact keys in examples and responses. <br>
Risk: The security scan reports that the skill lacks strong safeguards against accidental production use. <br>
Mitigation: Default operational reviews to the test environment and confirm environment, order hash, quantity, and action before executing production requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zschen211/stove-taker-api) <br>
- [Taker API](references/Taker API.md) <br>
- [API Authorization](references/API Authorization.md) <br>
- [Validate Order](references/Validate Order.md) <br>
- [Lock Order](references/Lock Order.md) <br>
- [Unlock Order](references/Unlock Order.md) <br>
- [Fill Order](references/Fill Order.md) <br>
- [Cancellation Response](references/Cancellation Response.md) <br>
- [Query Orders](references/Query Orders.md) <br>
- [Query Fill Records](references/Query Fill Records.md) <br>
- [Discover New Orders](references/Discover New Orders.md) <br>
- [WebSocket Real-time Push](references/WebSocket Real-time Push.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [API responses are printed to stdout; live actions require user-supplied Stove Taker API credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
