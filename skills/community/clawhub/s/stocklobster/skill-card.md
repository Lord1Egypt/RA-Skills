## Description: <br>
Monitor StockLobster webhook alerts through OpenClaw and route screened stock signals to chat channels such as Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[l3g](https://clawhub.ai/user/l3g) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and troubleshoot OpenClaw hook mappings that ingest StockLobster alerts and deliver screened stock signals to Telegram or another supported channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook endpoints and chat destinations can expose alerts or send messages to the wrong channel if tokens, URLs, or chat IDs are misconfigured. <br>
Mitigation: Use a dedicated hooks token, verify the Telegram chat ID, back up ~/.openclaw/openclaw.json, and expose the webhook endpoint only where StockLobster alerts should be received. <br>
Risk: OpenClaw templates that reference the wrong payload object can produce empty messages or failed delivery. <br>
Mitigation: Use payload fields such as {{payload.text}} for the confirmed simple payload and test the mapping with curl before relying on live alerts. <br>


## Reference(s): <br>
- [StockLobster Payload Format](references/payload-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown with JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for editing OpenClaw configuration and testing webhook delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
