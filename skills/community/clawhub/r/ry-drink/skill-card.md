## Description:

瑞玥餐饮API lets an agent query real-time restaurant data and perform reservation, ordering, order adjustment, cancellation, and payment-link workflows through configured tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhimibuhui](https://clawhub.ai/user/zhimibuhui)

### License/Terms of Use:

MIT-0

## Use Case:

External restaurant customers and merchant service agents use this skill to retrieve current shop information, menus, table availability, reservations, member balances, transactions, and dining orders. It can also create or modify reservations and orders, reduce or cancel orders, and generate payment links when the required customer and shop context is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change reservations and dining orders, including cancellations and item reductions.

Mitigation: Require explicit customer confirmation and disambiguation before reservation changes, cancellations, order reductions, and full-order cancellations.

Risk: The skill can create payment links for dining orders.

Mitigation: Confirm the active reservation or selected order before generating payment links, and rely on backend authorization for the linked order.

Risk: Customer and merchant context may be sent over plaintext internal HTTP.

Mitigation: Use HTTPS or a protected authenticated transport for live merchant deployments.

Risk: Reservation, order, member, and transaction operations expose object-level authorization risk.

Mitigation: Confirm backend object-level authorization on every reservation, order, member, and transaction operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhimibuhui/skills/ry-drink)
- [Tool router documentation](artifact/tool-router.md)
- [Tool manifest](artifact/tools.json)
- [Skill manifest](artifact/skill.json)

## Skill Output:

**Output Type(s):** [text, configuration, shell commands]

**Output Format:** [Plain text user responses backed by JSON tool results and configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Business replies are expected to hide tool names, internal identifiers, and execution traces from end users.]

## Skill Version(s):

1.0.31 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
