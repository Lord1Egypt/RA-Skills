## Description: <br>
Books same-city on-demand courier deliveries in China through Tencent Mobility MCP, including pickup and delivery booking, order queries, rider tracking, and cancellation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to guide an agent through same-city courier booking, payment, status lookup, rider tracking, and cancellation for Tencent Mobility delivery tasks in China. It is intended for runner-style parcel delivery, not cross-city shipping, food delivery, ride hailing, or finance queries. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a Tencent delivery token and delivery session details on disk. <br>
Mitigation: Use only in a trusted local environment, avoid sharing the workspace, and delete or rotate the token when access is no longer needed. <br>
Risk: Authenticated MCP access can book, query, and cancel courier orders. <br>
Mitigation: Confirm user intent before order-changing actions, rely on the documented workflow gates, and avoid using real payment links or sensitive addresses until the skill has been reviewed. <br>
Risk: Payment QR generation uses a third-party QR endpoint for payment URLs. <br>
Mitigation: Review the QR generation path before real transactions and prefer trusted payment handling where required by policy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tencent-adm/tencent-delivery-skill) <br>
- [Tencent Delivery Skill Instructions](SKILL.md) <br>
- [Delivery Workflow](references/delivery-workflow.md) <br>
- [Order Workflow](references/order-workflow.md) <br>
- [Quick Start Workflow](references/quick-start-workflow.md) <br>
- [MCP API Contract](references/api-contract.md) <br>
- [Session State](references/session-state.md) <br>
- [Error Handling](references/error-handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Configuration guidance] <br>
**Output Format:** [Markdown replies with inline shell commands and Tencent MCP-derived order information] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include payment QR markdown and sanitized courier status text; sensitive token, session, SKU, and internal identifier fields are not intended for user output.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
