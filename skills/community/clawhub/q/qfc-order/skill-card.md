## Description:

Automates QFC pickup shopping by adding unchecked grocery-list items to the online cart, adjusting quantities, presenting a cart review, and helping schedule a pickup slot through an attached logged-in Chrome tab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonahorn](https://clawhub.ai/user/jasonahorn)

### License/Terms of Use:


## Use Case:

External QFC shoppers use this skill to automate routine grocery pickup cart building and pickup-slot scheduling while retaining manual control over login, cart review, and final submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates in a logged-in QFC browser tab and can affect a real shopping cart.

Mitigation: Review the cart, quantities, prices, pickup slot, total, and any final submit action before confirming the order.

Risk: Local order-state details may retain shopping or transaction metadata.

Mitigation: Clear qfc-state.json after ordering if retained shopping or transaction metadata is not desired.

## Reference(s):

- [Qfc Order ClawHub Skill Page](https://clawhub.ai/jasonahorn/skills/qfc-order)
- [QFC Website](https://www.qfc.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown status updates, cart review text, and browser-session guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-attached logged-in Chrome tab and may save local order-state details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
