## Description: <br>
Auto-create and manage Whop digital products, pricing plans, and checkout links using the Whop REST API and a Company API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssidharhubble](https://clawhub.ai/user/ssidharhubble) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business operators use this skill to create Whop products, paid or free plans, and checkout links for digital product sales. It is intended for users who are ready to make live changes in a Whop business account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create live public products, pricing plans, and checkout links in a Whop business account. <br>
Mitigation: Review the product names, descriptions, prices, and visibility settings before running the script, and run it only when ready for live account changes. <br>
Risk: The skill uses a sensitive Whop Company API key. <br>
Mitigation: Store WHOP_API_KEY in a secret manager, prefer the narrowest available key scope, and avoid printing or committing the key. <br>


## Reference(s): <br>
- [Whop API Reference](https://docs.whop.com/api-reference/) <br>
- [Whop Developer Dashboard](https://sell.whop.com/developer) <br>
- [ClawHub Skill Page](https://clawhub.ai/ssidharhubble/whop-digital-sales) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Text] <br>
**Output Format:** [Markdown guidance with Python script execution and console status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WHOP_API_KEY; API calls can create public Whop products, pricing plans, and checkout links.] <br>

## Skill Version(s): <br>
1.0.14 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
