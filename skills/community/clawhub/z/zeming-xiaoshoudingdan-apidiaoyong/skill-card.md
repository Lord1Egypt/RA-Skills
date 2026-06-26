## Description: <br>
Presents DingTalk-style order data for review, showing 20 order fields and offering confirm, retry, or exit choices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duanzhen001](https://clawhub.ai/user/duanzhen001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales or operations staff can use this skill to review customer order details before continuing an order workflow. Evidence flags embedded customer and contact details and unclear chained behavior, so it should be reviewed and sanitized before real order processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds real-looking customer order and contact details. <br>
Mitigation: Remove embedded customer data, replace it with placeholders or an authorized DingTalk lookup, and mask sensitive fields by default before use. <br>
Risk: The workflow claims DingTalk import behavior and includes automatic chaining to a second skill without clearly identifying that second skill. <br>
Mitigation: Clearly document and review the chained skill behavior before enabling workflow chaining for real order processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/duanzhen001/zeming-xiaoshoudingdan-apidiaoyong) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/duanzhen001) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text console output with A/B/C workflow choices] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Displays 20 order fields and branches based on confirm, retry, or exit selection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
