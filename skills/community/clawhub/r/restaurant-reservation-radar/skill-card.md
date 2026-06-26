## Description: <br>
旅行目的地米其林与热门餐厅空位监控、自动预约与定金提醒助手。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lmercy](https://clawhub.ai/user/lmercy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers use this skill to monitor Michelin and popular restaurant availability for a destination, match options to trip dates and dining preferences, and receive reservation status, confirmation, deposit, or fallback guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can monitor reservation platforms and act using personal contact details. <br>
Mitigation: Require explicit user confirmation before each booking submission and before sharing contact details with any reservation platform or notification service. <br>
Risk: Reservation flows may request verification codes, card guarantees, deposits, or payment. <br>
Mitigation: Pause for user approval before using verification codes, card details, guarantees, deposits, or any payment-related step. <br>
Risk: Collected phone numbers, email addresses, and booking details may expose sensitive travel or contact information. <br>
Mitigation: Mask contact details in responses, avoid persistent storage, and provide a clear stop-monitoring command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lmercy/restaurant-reservation-radar) <br>
- [Platform reference manual](reference.md) <br>
- [Usage examples](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-style conversational responses, structured restaurant lists, status updates, and notification templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include reservation options, confirmation prompts, masked contact details, deposit warnings, and fallback recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
