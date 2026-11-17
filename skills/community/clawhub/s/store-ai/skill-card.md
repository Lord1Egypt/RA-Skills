## Description:

Chinese-language store-management assistant for Shejian Hong Kong that helps staff interpret store operation requests and prepare inventory, sales, purchasing, account, and weather API actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xingke2023](https://clawhub.ai/user/xingke2023)

### License/Terms of Use:

MIT-0

## Use Case:

Store staff and operators use this agent to convert Chinese natural-language updates and questions into confirmed store-management actions for inventory lookup, sales supplement records, purchase intake, sales reports, account checks, and weather context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer tokens and user-derived fields may be placed directly into shell curl commands for sensitive store actions.

Mitigation: Use least-privilege, revocable tokens; redact Authorization headers; and replace shell-built requests with a structured HTTP client or secret-aware tool before deployment.

Risk: Untrusted product names, notes, or other free-text fields could be unsafe while shell-based command construction is used.

Mitigation: Limit use to trusted operators and safely validate or serialize free-text fields before allowing execution.

Risk: The skill can prepare sensitive business write actions such as sales supplements, inventory adjustments, and purchase orders.

Mitigation: Require explicit confirmation before write actions and review account permissions and operation logs regularly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xingke2023/skills/store-ai)
- [Store management API base URL](https://s.xingke888.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese user-facing text with confirmation summaries, formatted results, and inline curl command structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write operations are expected to present a confirmation summary before execution.]

## Skill Version(s):

1.0.6 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
