## Description: <br>
ZeeLin 闲鱼自运营 helps sellers operate a logged-in Xianyu web session by drafting buyer replies, negotiation responses, listing copy, sales follow-up language, and browser-assisted actions that require user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelcey2023](https://clawhub.ai/user/kelcey2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketplace sellers use this skill to handle Xianyu customer-service and listing workflows, including reply drafts, price-negotiation wording, item descriptions, follow-up messages, and confirmed browser-side publishing or sending actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can view and operate a logged-in Xianyu browser session. <br>
Mitigation: Use it only with an intended account session and review the selected chat, item, price, and final text before approving any send, edit, or publish action. <br>
Risk: A wrong conversation, seller or buyer role, item, or price could lead to an inappropriate marketplace reply. <br>
Mitigation: Confirm the current conversation identity, item details, recent message context, and seller/buyer role before sending; stop and ask the user when details do not match. <br>
Risk: Batch replies can create account or customer-service risk in disputes, high-value transactions, or unclear conversations. <br>
Mitigation: Keep confirmation enabled, process small batches, and avoid direct batch sending for disputes, high-value items, or ambiguous conversations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kelcey2023/zeelin-xianyu-auto-ops) <br>
- [Xianyu Web Marketplace](https://www.goofish.com/) <br>
- [Browser Execution SOP](references/browser-sop.md) <br>
- [Listing Playbook](references/listing-playbook.md) <br>
- [Reply Playbook](references/reply-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown drafts, concise recommendations, browser-operation steps, and simple JSON from the message classifier script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires review and confirmation before account-affecting sends, edits, or publishes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
