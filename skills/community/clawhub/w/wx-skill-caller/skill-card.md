## Description: <br>
WX Skill Caller forwards general user message text to a configured wx backend API and returns the backend JSON response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heqq-github](https://clawhub.ai/user/heqq-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or agents use this skill to route free-form chat, Chinese questions, general help requests, and open-ended text to a wx backend service, except when the request explicitly requires local tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Raw user messages may be sent to a third-party backend across broad routing cases without clear per-message consent. <br>
Mitigation: Enable this skill only when users understand that ordinary chat text may be forwarded; avoid secrets, credentials, private business data, and personal information, and prefer opt-in routing with redaction or confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heqq-github/wx-skill-caller) <br>
- [wx backend API endpoint](https://test-gig-c-api.1haozc.com/api/wx/kjj/v1/customer/skill/call) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Shell commands, Guidance] <br>
**Output Format:** [JSON response rendered as agent text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Forwards the raw message content field to the backend API; script timeout is 30 seconds.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
