## Description: <br>
Chinese-language assistant skill that silently caches same-day order details and formats the current order set only when explicitly asked to organize current orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lemonjuice0](https://clawhub.ai/user/lemonjuice0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or operations staff can use this skill to collect same-day order messages silently and produce a fixed customer notification, internal execution block, and table-import row when the explicit trigger is received. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Order messages may contain customer or transaction details that should not be retained longer than necessary. <br>
Mitigation: Avoid entering unnecessary sensitive customer details, and use the clear-cache command when order information should be discarded. <br>
Risk: The skill intentionally remains silent until the exact trigger, which can make cached state less visible to users. <br>
Mitigation: Use it only where silent order collection is desired and confirm the final formatted output before using it operationally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lemonjuice0/task-assistant-bot) <br>
- [Publisher profile](https://clawhub.ai/user/lemonjuice0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Chinese Markdown-like fixed-format order summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs only on the exact organize-current-orders trigger; missing order fields are filled as pending when cached order data exists.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
