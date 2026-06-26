## Description: <br>
Detects large cbBTC whale movements on Base within 4 hours, indicating accumulation, distribution, or neutral Bitcoin market signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kokoju007](https://clawhub.ai/user/kokoju007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and crypto analysts use this skill to ask an agent for recent cbBTC whale activity on Base, direction hints, and a short informational market-signal summary. Paid Orion ACP calls may provide full transaction data and structured JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides informational crypto market signals that users could over-weight for trading decisions. <br>
Mitigation: Treat whale classifications as one input only and do not rely on them alone for trading decisions. <br>
Risk: The skill routes users toward paid Orion ACP offerings. <br>
Mitigation: Confirm the ACP offering name, price, expected output, and user intent before any paid call. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kokoju007/whale-radar-orion) <br>
- [Orion ACP listing](https://app.virtuals.io/virtuals/1809) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown text with optional structured JSON from paid ACP offerings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free output summarizes whale activity, direction classification, and a short market-signal note; paid offerings may include transaction amounts, wallet addresses, token flows, and structured JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
