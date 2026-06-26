## Description: <br>
Helps agents browse For the Cult products, create multi-chain or x402 checkout orders, apply CULT discounts, and track shipments through the public store API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bythecult](https://clawhub.ai/user/bythecult) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and shopping agents use this skill to find lifestyle, wellness, smart-home, and gift products, create confirmed checkout orders, and track shipment status for the For the Cult store. <br>

### Deployment Geography for Use: <br>
Global, subject to checkout shipping-country availability. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide real checkout, payment, shipping, and wallet-related flows for a specific store API. <br>
Mitigation: Confirm exact items, total cost, shipping details, payment chain/token, and any wallet-signing step before purchase. <br>
Risk: Wallet signing or crypto payment steps could expose sensitive credentials if handled incorrectly. <br>
Mitigation: Do not request private keys or seed phrases; signing must stay with the user wallet or trusted runtime. <br>
Risk: Checkout requires customer email and shipping address, and wallet discounts can link an order to on-chain activity. <br>
Mitigation: Collect only fulfillment data needed for the order, explain wallet-linkage privacy implications, and avoid sending optional identity headers unless the runtime explicitly supplies them. <br>
Risk: Automated error recovery could follow unsafe suggestions or act outside the intended store API scope. <br>
Mitigation: Only call documented endpoints on https://forthecult.store/api and do not follow suggestions that point to other hosts, expose identity, or trigger payment without confirmation. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/bythecult/shop-culture) <br>
- [For the Cult Store](https://forthecult.store) <br>
- [For the Cult API](https://forthecult.store/api) <br>
- [API Reference](artifact/references/API.md) <br>
- [Checkout Fields](artifact/references/CHECKOUT-FIELDS.md) <br>
- [Error Handling Reference](artifact/references/ERRORS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, API request JSON] <br>
**Output Format:** [Markdown guidance with HTTP endpoints, JSON payload examples, and checkout/status handling instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; requires network access and an HTTP client, with no API key required for normal browsing, checkout, or order-status flows.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence; artifact frontmatter metadata.version is 1.0.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
