## Description: <br>
Robinhood helps agents organize public Robinhood product, fee, help, risk, and announcement information without account access, trading, or financial advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike47512](https://clawhub.ai/user/mike47512) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to summarize public Robinhood pages covering products, fees, account capabilities, restrictions, help resources, risk notices, and announcements. It is not for private account access, transaction execution, investment advice, lending advice, or tax advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public financial-service information may be outdated or region-specific. <br>
Mitigation: Verify important details on Robinhood's official pages and include page dates and applicable regions in outputs. <br>
Risk: Summaries of Robinhood products, fees, or risks could be mistaken for investment, lending, or tax advice. <br>
Mitigation: Keep outputs descriptive, label them as public-information summaries, and avoid recommendations or personalized financial conclusions. <br>
Risk: Users may attempt to provide credentials, balances, identity details, bank information, or private transaction data. <br>
Mitigation: Do not request or process private account data, login-state pages, credentials, fund-transfer requests, or trade instructions. <br>


## Reference(s): <br>
- [Robinhood homepage](https://robinhood.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown summaries, tables, and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should cite public source pages, include page dates and applicable regions when relevant, and avoid private account data or financial advice.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
