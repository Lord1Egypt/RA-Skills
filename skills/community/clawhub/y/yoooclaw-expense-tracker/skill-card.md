## Description: <br>
从手机通知中提取个人已发生的消费流水（外卖、快递、缴费、购物、打车、加油、信用卡还款、转账等），按类目和时间汇总并给出总额。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External individual users use this skill to summarize real spending from phone notification history by time period and category, including food delivery, shopping, transit, utilities, credit card repayment, transfers, and refunds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read broad notification history that may include sensitive financial and personal messages. <br>
Mitigation: Use explicit spending-summary requests with narrow date ranges and, when possible, a specific source or category scope. <br>
Risk: Vague prompts may cause private notifications outside the intended spending question to be searched. <br>
Mitigation: Ask for a defined period and category, and provide an explicit notification data path only for the records intended for analysis. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/vivalavida-say-hi/yoooclaw-expense-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/vivalavida-say-hi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown spending summaries with category totals, date-level detail, transfer separation, refund adjustments, and pending-confirmation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request a notification data path if the local notification storage command is unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
