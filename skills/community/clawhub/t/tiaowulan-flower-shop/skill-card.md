## Description: <br>
A flower-ordering agent that helps users browse bouquets, view product details, get occasion-based recommendations, place flower delivery orders, and confirm order results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[piaoleaf](https://clawhub.ai/user/piaoleaf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to choose flowers for delivery, provide recipient and delivery details, submit an order, and receive payment guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create real flower delivery orders and send recipient name, phone number, address, card text, and delivery time to an external order API. <br>
Mitigation: Before submitting, confirm the product, price, recipient details, delivery time, external data sharing, and permission to use the recipient information. <br>
Risk: The security review notes no clear final privacy or consent step before personal details are sent. <br>
Mitigation: Add an explicit final confirmation that lists the personal data and destination service before any order submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/piaoleaf/tiaowulan-flower-shop) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown product cards, order summaries, and inline curl command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit recipient and order details to an external flower-ordering service and return payment guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
