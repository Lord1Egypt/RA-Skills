## Description: <br>
Production-ready WhatsApp ordering agent for restaurants and QSRs that handles natural-language orders, provides Subway-style recommendations and upsells, reads menus from Google Sheets, logs orders, and uses ThumbGate safety rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igorganapolsky](https://clawhub.ai/user/igorganapolsky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Restaurant operators and QSR teams use this skill to run a WhatsApp ordering assistant that can answer menu questions, take and confirm customer orders, suggest bounded upsells, and log order details to Google Sheets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live WhatsApp orders and stores customer phone and order data in Google Sheets without clear privacy or control boundaries. <br>
Mitigation: Use a dedicated WhatsApp number and least-privilege Google Sheet, add a customer privacy notice and consent language, and define retention and deletion rules before production use. <br>
Risk: Ambiguous or high-risk customer interactions may require human judgment. <br>
Mitigation: Require human handoff for ambiguous or high-risk cases and follow the documented frustration fallback behavior. <br>
Risk: The setup guide invokes an external ThumbGate package with npx. <br>
Mitigation: Verify the external ThumbGate package before running the npx setup command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/igorganapolsky/subway-restaurant-agent) <br>
- [Setup guide](artifact/setup-guide.md) <br>
- [ThumbGate prevention rules](artifact/thumbgate-rules.md) <br>
- [ElevenLabs affiliate page](https://elevenlabs.io/affiliates) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions, Shell commands, Text] <br>
**Output Format:** [Markdown instructions with inline shell commands and operational rules] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent behavior guidance for WhatsApp ordering, Google Sheets menu and order logging, upsell boundaries, and human handoff conditions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
