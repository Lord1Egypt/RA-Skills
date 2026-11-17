## Description:

TravelKit flight booking and management skill. Use for flight search, pricing, real-time price verification, order creation, payment, cancellation, refund, change, itinerary download, and TravelKit MCP integration policy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[travelkit](https://clawhub.ai/user/travelkit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to search flights, verify live prices, create and manage flight orders, handle payments, cancellations, refunds, changes, invoices, and itinerary downloads through TravelKit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel, passenger, order, invoice, and payment-flow data may be sent to TravelKit MCP tools during normal use.

Mitigation: Install only for TravelKit flight workflows and rely on platform-managed credentials; do not ask users to paste API keys or secrets in chat.

Risk: Flight order creation, payment, cancellation, refund, change, and invoice creation can affect real bookings or financial flows.

Mitigation: Require explicit user confirmation for each write action, verify live price before collecting passenger details, and re-check order status before risky payment retries.

Risk: Default consumer output is Simplified Chinese with CNY-oriented price presentation.

Mitigation: Review locale expectations before deployment and switch language or locale only when the user or host context requires it.

Risk: Tool results may include internal identifiers, raw JSON, credentials, or booking record fields that are not appropriate for normal users.

Mitigation: Summarize results in user-facing language and omit internal fields, raw MCP responses, API keys, passenger IDs, segment IDs, solution IDs, order keys, and PNR values.

## Reference(s):

- [TravelKit](https://www.travelkit.ai/)
- [confirmation-rules](references/confirmation-rules.md)
- [flight-search](references/flight-search.md)
- [flight-pricing](references/flight-pricing.md)
- [flight-verify](references/flight-verify.md)
- [flight-create-order](references/flight-create-order.md)
- [flight-pay-order](references/flight-pay-order.md)
- [flight-order-lookup](references/flight-order-lookup.md)
- [flight-invoice](references/flight-invoice.md)
- [flight-cancel](references/flight-cancel.md)
- [flight-refund](references/flight-refund.md)
- [flight-change](references/flight-change.md)
- [flight-itinerary](references/flight-itinerary.md)
- [mcp-connection](references/mcp-connection.md)
- [output-rules](references/output-rules.md)
- [hidden-fields](references/hidden-fields.md)
- [tool-categories](references/tool-categories.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API Calls]

**Output Format:** [Simplified Chinese Markdown with structured flight, order, payment, refund, change, invoice, and itinerary summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Consumer replies default to Simplified Chinese and CNY pricing unless the user requests another language or locale.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
