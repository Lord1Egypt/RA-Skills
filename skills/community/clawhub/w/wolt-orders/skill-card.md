## Description: <br>
Discover restaurants with advanced filters, place single or group orders on Wolt.com, reorder past favorites, track status in real time, detect delays, contact support, and send updates to Slack or other connected channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dviros](https://clawhub.ai/user/Dviros) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to browse Wolt restaurants, build and confirm food orders, coordinate group orders, track delivery status, and route order updates or support interactions to connected channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a logged-in Wolt browser session and place real orders after confirmation. <br>
Mitigation: Before confirming checkout, verify the restaurant, items, quantities, delivery address, total, payment method, and that the user explicitly approved the order. <br>
Risk: Order status, tracking details, or support messages may be shared to connected channels. <br>
Mitigation: Use only the intended private channel and confirm the exact notification destination before sending order updates. <br>
Risk: Support contact can send messages about an order through the user's account. <br>
Mitigation: Review the support message content with the user and get approval before sending. <br>


## Reference(s): <br>
- [Wolt](https://wolt.com) <br>
- [Wolt Israel example region](https://wolt.com/il) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries, tables, confirmations, tracking updates, support-message drafts, and channel notifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires browser-enabled execution and explicit user confirmation before checkout or support messaging.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
