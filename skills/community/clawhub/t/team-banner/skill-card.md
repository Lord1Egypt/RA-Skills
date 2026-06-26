## Description: <br>
为中文用户根据团队特点和活动类型生成团建横幅标语，并在生成前引导完成付费订单。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liulian822](https://clawhub.ai/user/liulian822) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to create short Chinese banner slogans for team-building, annual meetings, outdoor training, sales teams, and similar group activities after confirming the payment details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment records and identifiers may not match the advertised team-banner service. <br>
Mitigation: Before paying, confirm the payee, amount, service slug, and order description match the expected team-banner service. <br>
Risk: The artifact asks the agent to disclose its thought process. <br>
Mitigation: Remove that instruction and provide only user-facing reasoning or results. <br>
Risk: Order data is saved locally without documented cleanup. <br>
Mitigation: Review stored order files and define a retention or cleanup process before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liulian822/team-banner) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/liulian822) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese text with order status fields and a generated banner slogan] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires payment/order confirmation before slogan generation; artifact behavior stores order data locally.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
