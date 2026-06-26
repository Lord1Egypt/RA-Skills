## Description: <br>
A specialized tool for sending quantitative trading signals to the FMZ platform via HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[13290186019](https://clawhub.ai/user/13290186019) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and trading automation developers use this skill to send buy, sell, wait, or close signals from an agent to an FMZ trading robot. It is intended for structured signal delivery, not for independently validating market strategy or trade suitability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger real trading signals. <br>
Mitigation: Use it only with a test or paper-trading FMZ robot until configuration and approval controls are verified. <br>
Risk: The default UUID and broad robot targeting can weaken signal scoping. <br>
Mitigation: Replace the default UUID with a private secret and avoid broadcast node_id 0 unless intentionally targeting all robots. <br>
Risk: Buy, sell, or close actions may reach a live account without clear confirmation guardrails. <br>
Mitigation: Require manual approval before any trading signal is sent to a live account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/13290186019/send-signal) <br>
- [FMZ channel API endpoint](https://www.fmz.com/api/v1/channel) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls] <br>
**Output Format:** [Status string after posting JSON to the FMZ channel API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends action, symbol, price, and reason fields to FMZ using a configured UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
