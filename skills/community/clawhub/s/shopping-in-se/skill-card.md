## Description: <br>
Assists users with searching trusted Swedish e-commerce sites, adding items to cart, and completing checkout with approved payment details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caoqi](https://clawhub.ai/user/caoqi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to find and purchase products from trusted Swedish pharmacy, grocery, household, and general e-commerce sites. It is intended for shopping flows where the user explicitly confirms the item, recipient details, merchant, and price before an order is placed. <br>

### Deployment Geography for Use: <br>
Sweden <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read stored personal and payment data while assisting with purchases. <br>
Mitigation: Remove live or hardcoded card values, avoid storing card details in plaintext files, and use only a designated payment card with strict limits. <br>
Risk: The skill can automate real checkout payments using low-level browser control. <br>
Mitigation: Require explicit user approval immediately before any payment-submitting action, and verify the merchant, domain, product, price, and recipient details before checkout. <br>
Risk: Shopping through unknown or spoofed merchants could expose users to fraud or incorrect purchases. <br>
Mitigation: Use only the trusted merchant list, reject paid search ad links and unknown domains, require HTTPS, and check that prices are reasonable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/caoqi/shopping-in-se) <br>
- [Trusted Shopping Sites](references/trusted-sites.md) <br>
- [CDP Coordinate Click](references/cdp-click.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
