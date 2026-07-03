## Description: <br>
RollingGo hotel skill helps agents search, compare, and book hotels, check real-time room prices and cancellation terms, and monitor hotel price changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rollinggo-ai](https://clawhub.ai/user/rollinggo-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill through an agent to find hotels by location, budget, amenities, or brand, compare available rooms, and proceed through booking. It also supports checking existing hotel orders and monitoring selected hotels for price changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install executable hotel CLI tooling in the local environment. <br>
Mitigation: Review the skill and installation path before use, and install only when the user accepts the publisher's tooling. <br>
Risk: The skill can create real hotel booking orders and payment links. <br>
Mitigation: Before booking, show the exact hotel, room, dates, total price, cancellation terms, and contact details, then require explicit user confirmation. <br>
Risk: Order-history commands can expose past travel and contact information in the agent session. <br>
Mitigation: Use order-history features only when the user intentionally requests them and understands that travel and contact details may be shown. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rollinggo-ai/skills/rollinggo-hotel-skill-cn-new) <br>
- [CLI command parameter reference](references/cli-params.md) <br>
- [RollingGo Hotel CLI releases](https://github.com/RollingGo-AI/oauth-hotel-cli/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with user-facing hotel details, booking links, and CLI-backed guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include hotel names, prices, cancellation terms, payment links, order status, and price-monitoring recommendations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
