## Description:

ZeeLin 闲鱼自运营 helps agents support a logged-in Xianyu/Goofish web session with buyer reply drafts, negotiation responses, listing copy, listing optimization, common post-sale or pickup language, batch conversation review, and browser-assisted marketplace operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelcey2023](https://clawhub.ai/user/kelcey2023)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace sellers use this skill to draft and confirm Xianyu/Goofish buyer replies, negotiation responses, item listings, and browser-assisted store operations from an already logged-in web session. It is intended to keep human review enabled for sends, publishing, prices, after-sales promises, and conversation identity checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent could act in the wrong account, product, buyer/seller role, or conversation when operating a logged-in marketplace browser session.

Mitigation: Confirm the account, product, role, and conversation before any send or publish action, and stop for user confirmation when the page context does not match the requested task.

Risk: Generated replies could include incorrect prices, after-sales promises, or marketplace actions the seller did not approve.

Mitigation: Keep review enabled for replies, prices, after-sales commitments, and publishing; use drafts by default and require explicit approval before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kelcey2023/skills/zeelin-xianyu-auto-ops)
- [Publisher Profile](https://clawhub.ai/user/kelcey2023)
- [Xianyu/Goofish Web](https://www.goofish.com/)
- [买家回复与议价手册](references/reply-playbook.md)
- [商品上新与文案手册](references/listing-playbook.md)
- [浏览器执行 SOP](references/browser-sop.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with reply drafts, listing copy, operational guidance, and optional JSON intent classification]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed before marketplace send, publish, price, or after-sales actions.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact _meta.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
