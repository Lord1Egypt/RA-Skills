## Description: <br>
Real-time football transfer intelligence — rumours, credibility scores, and multi-source verification <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leeleon](https://clawhub.ai/user/leeleon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and football analysts use this skill to retrieve trending transfer rumours, player-specific transfer detail, and Truth Meter credibility checks from Rising Transfers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Player and club search terms are sent to Rising Transfers for transfer lookups and credibility checks. <br>
Mitigation: Install and use the skill only when sharing those search terms with Rising Transfers is acceptable. <br>
Risk: Authenticated detailed lookups and Truth Meter checks may use RT_API_KEY and consume account credits. <br>
Mitigation: Review credit usage expectations before detailed queries and keep RT_API_KEY scoped to this provider. <br>
Risk: The skill may be invoked automatically for transfer-news questions. <br>
Mitigation: Disable skill auto-discovery when each lookup should be approved manually. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leeleon/rising-transfers-transfer-intel) <br>
- [Rising Transfers API](https://api.risingtransfers.com) <br>
- [Rising Transfers API Docs](https://api.risingtransfers.com/docs) <br>
- [Rising Transfers Pricing](https://api.risingtransfers.com/pricing) <br>
- [Rising Transfers Privacy Policy](https://risingtransfers.com/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries with transfer details, credibility scores, source lists, and user-facing error guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Rising Transfers endpoints and may consume credits for detailed lookups and Truth Meter checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
