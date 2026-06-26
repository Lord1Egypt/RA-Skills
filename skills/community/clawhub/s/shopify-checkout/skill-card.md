## Description: <br>
Complete online shopping purchases on online stores through the Credpay Checkout API with x402 payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jelilat](https://clawhub.ai/user/jelilat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents assisting users with online purchases use this skill to collect required checkout details, request a quote, submit an x402 payment-backed checkout, and report order status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The checkout flow can send personal shipping and contact details to a third-party Credpay endpoint. <br>
Mitigation: Confirm the merchant, item, quantity, total price, destination address, and contact details with the user before submitting checkout data. <br>
Risk: The skill can trigger payment-linked checkout and may require additional authorization if the order total exceeds the quote. <br>
Mitigation: Require an explicit user confirmation step for initial and additional x402 payment authorization, and stop instead of blind-retrying failed orders. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jelilat/shopify-checkout) <br>
- [Credpay Checkout API endpoint](https://checkout-agent.credpay.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Text] <br>
**Output Format:** [Markdown guidance with HTTP request examples and JSON status responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns checkout request IDs, polling status, completed order details, or failure codes and messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
