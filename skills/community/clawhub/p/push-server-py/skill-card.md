## Description: <br>
Send notifications to WeCom users through a Push Server OpenAPI service with TEXT, MARKDOWN, TEXT_CARD, and NEWS message types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[es-v](https://clawhub.ai/user/es-v) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send WeCom notifications from an agent workflow through a configured Push Server endpoint. It is suited for operational alerts, report links, status updates, and article-style notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notification recipients, message content, links, or operational details may be printed to command output before sending. <br>
Mitigation: Review logs before production use and redact or remove full request-body printing when notification payloads may contain private or sensitive information. <br>
Risk: The skill sends notification payloads and an API key to a configured push server endpoint. <br>
Mitigation: Use a trusted HTTPS endpoint and a least-privilege API key stored in the required environment variable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/es-v/push-server-py) <br>
- [Push Server project](https://github.com/qingzhou-dev/push-server) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API Calls, JSON, Guidance] <br>
**Output Format:** [JSON responses and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus QYWX_PUSH_API_KEY and QYWX_PUSH_URL environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
