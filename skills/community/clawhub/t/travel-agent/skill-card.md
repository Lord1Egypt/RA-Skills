## Description: <br>
Find, book, and change flights for your human via email. One message, and done. (by BonBook) <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aSzelem](https://clawhub.ai/user/aSzelem) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and their agents use this skill to search, book, change, and cancel flights through BonBook by sending and receiving booking email with explicit human approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an agent with email send and receive access, which may expose mailbox content beyond BonBook-specific messages. <br>
Mitigation: Install only for trusted agents with appropriate mailbox access controls, and limit use to BonBook-related messages and booking operations. <br>
Risk: Flight booking, changes, cancellation, payment, calendar sync, and PII entry can affect travel plans, money, and personal data. <br>
Mitigation: Require explicit human review and approval for itinerary choices, prices, refund terms, payment steps, calendar sync, and any PII entry. <br>
Risk: Email should not contain passport numbers, card numbers, credentials, or unnecessary personal data. <br>
Mitigation: Keep sensitive data on BonBook web flows or secure portals and avoid placing sensitive PII or payment details in email. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aSzelem/travel-agent) <br>
- [BonBook website](https://bonbook.co) <br>
- [BonBook access setup](https://bonbook.co/access) <br>
- [artifact/README.md](artifact/README.md) <br>
- [artifact/skill.md](artifact/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Email instructions, Configuration] <br>
**Output Format:** [Markdown instructions with example email text and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires existing email send and receive permissions; optional web browsing, calendar read, and form completion may be used with explicit human approval.] <br>

## Skill Version(s): <br>
2.4.1 (source: skill metadata and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
