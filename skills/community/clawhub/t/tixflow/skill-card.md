## Description: <br>
AI-powered event assistant for discovering, booking, and coordinating event tickets with KYD Labs protocol and Google Calendar integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Seenfinity](https://clawhub.ai/user/Seenfinity) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use TixFlow to search for events, compare prices, coordinate waitlists and calendar entries, and prototype ticket purchase flows for OpenClaw agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises ticket buying, wallet or NFT minting, calendar, and routing powers without clear consent or safety boundaries. <br>
Mitigation: Do not connect payment, wallet, calendar, or minting credentials until purchases and account changes require explicit confirmation and data sharing is documented. <br>
Risk: Mock ticket, transaction, calendar, and event data could be mistaken for real outcomes. <br>
Mitigation: Label mock and demo results clearly, validate event and purchase status through trusted services, and avoid acting on generated identifiers as completed transactions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Seenfinity/tixflow) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill manifest](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, API calls] <br>
**Output Format:** [JSON-like function results and short natural-language responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires external API credentials for calendar, maps, ticketing, and minting flows; mock/demo results may be returned when real integrations are not configured.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
