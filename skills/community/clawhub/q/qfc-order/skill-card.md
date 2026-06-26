## Description: <br>
Automates QFC grocery pickup ordering by adding unchecked grocery-list items to a logged-in QFC cart, reviewing quantities and prices, and helping schedule a pickup slot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasonahorn](https://clawhub.ai/user/jasonahorn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
QFC pickup shoppers use this skill to have an agent add unchecked grocery-list items to an online cart, summarize cart details, and assist with pickup-slot selection while the user stays involved in final order decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act inside a logged-in QFC shopping session. <br>
Mitigation: Watch the browser session and require explicit user confirmation before any final submit or place-order action. <br>
Risk: Cart contents, substitutions, slot, fees, or total may differ from the intended grocery list. <br>
Mitigation: Verify the store, items, quantities, substitutions, pickup slot, fees, and total during the cart and final reviews. <br>
Risk: Order details may remain in local state after use. <br>
Mitigation: Disconnect the browser relay and clear qfc-state.json if retained order details are not wanted. <br>


## Reference(s): <br>
- [Qfc Order on ClawHub](https://clawhub.ai/jasonahorn/qfc-order) <br>
- [QFC](https://www.qfc.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown status updates, cart review text, browser-action guidance, and JSON state updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an attached logged-in Chrome tab and user confirmation before final order placement.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
