## Description: <br>
Sends WhatsApp one-time password messages through the CMI OmniChannel RCS API using a preconfigured template. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[picccabo-art](https://clawhub.ai/user/picccabo-art) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations teams use this skill to send WhatsApp verification or authentication codes through CMI CPaaS when they have approved tenant and application credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles OTP-sending credentials and application secrets. <br>
Mitigation: Use least-privilege or test CMI credentials, avoid placing long-lived secrets in chat or shell history, and rotate credentials according to operational policy. <br>
Risk: The server security summary reports disabled normal network protections, including TLS verification changes and proxy bypass behavior. <br>
Mitigation: Review before installing, confirm the recipient before sending, and do not use in production unless the security or operations team accepts the network behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/picccabo-art/whatsapp-otp) <br>
- [CMI OmniChannel RCS singleSend endpoint](https://cpaas-rcs.cmidict.com:7081/singleSend) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell command invocations and plain-text script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends one WhatsApp OTP per invocation and requires CMI tenant credentials, application credentials, recipient number, and OTP code.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
