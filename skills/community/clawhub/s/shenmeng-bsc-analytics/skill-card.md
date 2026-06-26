## Description: <br>
BSC Analytics helps agents analyze BNB Chain DeFi protocols, evaluate projects, calculate yield scenarios, and surface BSC ecosystem risk signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and crypto users can use this skill for BNB Chain ecosystem research, protocol and project evaluation, and yield scenario calculations. Its analytics should be reviewed as static sample research, not live BSC monitoring or financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Analytics and yield outputs may be static sample research rather than live BSC monitoring or financial advice. <br>
Mitigation: Review outputs against current market and on-chain data before acting, and treat recommendations as research support only. <br>
Risk: The skill includes an under-disclosed paid verification flow that may ask for a wallet address and contact an external SkillPay service. <br>
Mitigation: Avoid providing a wallet address unless intentionally using the paid flow; the publisher should disclose the external payment data flow. <br>
Risk: The security evidence reports an exposed payment API key and recommends changing how payment verification is handled. <br>
Mitigation: The publisher should rotate the exposed key and move payment verification server-side or into secure configuration. <br>
Risk: The security evidence says the skill overstates live monitoring capabilities. <br>
Mitigation: Confirm which monitoring features are actually implemented before relying on the skill for operational monitoring. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenmeng/shenmeng-bsc-analytics) <br>
- [Publisher profile](https://clawhub.ai/user/shenmeng) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline code blocks, command examples, and script-generated JSON-style analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes BSC ecosystem summaries, protocol/project evaluations, yield calculations, and risk notes; some script outputs use static sample data.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
