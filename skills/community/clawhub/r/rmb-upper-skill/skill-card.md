## Description: <br>
人民币大写转换工具，将数字金额转换为人民币大写字符串。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[q342998378](https://clawhub.ai/user/q342998378) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and finance operations users can convert numeric RMB amount strings into uppercase Chinese currency text for forms, invoices, accounting workflows, and internal tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RMB uppercase conversion output could be unsuitable as the sole source of truth for contracts, invoices, or accounting records. <br>
Mitigation: Verify converted amounts against authoritative financial systems or human review before relying on them in formal documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/q342998378/rmb-upper-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [JSON object containing a success flag and either a text RMB uppercase amount string or an error message.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts one amount string and supports integer, decimal, and negative RMB amounts.] <br>

## Skill Version(s): <br>
1.0.0 (source: manifest.yaml and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
