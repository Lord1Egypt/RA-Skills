# ThumbGate Prevention Rules – Subway Restaurant Agent

1. **No Hallucinated Menu Items** — Block any response that suggests an item not present in the current Google Sheet.
2. **Always Confirm Before Finalizing** — Block any message that says “order placed” without first summarizing the full order and getting explicit confirmation.
3. **Upsell Limits** — Block upsell suggestions that would increase the total by more than 40% in one message.
4. **No Double Upselling** — If customer says “no thanks,” block any follow-up upsell in the same conversation turn.
5. **Mandatory Order Logging** — Block any conversation end that does not include a successful Google Sheets log entry.
6. **Frustration Fallback** — If sentiment analysis detects frustration, immediately block further selling and offer human handoff.
7. **Price Transparency** — Never quote a total without itemizing it first.
8. **Rush-Hour Priority** — During peak hours (user-defined), prioritize speed over extra upsells.
9. **No Over-Promising** — Block any promise about delivery/ready time that isn’t backed by current data.
10. **Error Recovery** — On any API or Sheet error, log it and immediately offer to text a human.
