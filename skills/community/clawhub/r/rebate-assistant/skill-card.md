## Description: <br>
返利宝 routes rebate-related shopping requests across authorization and tutorials, product-link rebate conversion, and product search for Taobao, JD, and Pinduoduo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skyfile](https://clawhub.ai/user/skyfile) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers use this skill to complete WeChat authorization, submit Taobao/JD/Pinduoduo product links, search for products, generate rebate links, check rebate balances, and request withdrawals after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores rebate account binding data locally and uses it for balance, link, and withdrawal flows. <br>
Mitigation: Install only after user consent to local account-binding storage; document where binding data is stored and how users can clear it. <br>
Risk: Shopping text and product links may be sent to rebate and model services. <br>
Mitigation: Disclose the external services involved and avoid submitting sensitive or unrelated personal information in shopping requests. <br>
Risk: Withdrawal requests can be submitted after a confirmation phrase. <br>
Mitigation: Keep the confirmation step explicit, show the requested amount before submission, and require review of withdrawal behavior before deployment. <br>
Risk: The scanner found limited scoping disclosure for account and privacy behavior. <br>
Mitigation: Add clear retention, data-use, and consent guidance before distributing the skill broadly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skyfile/rebate-assistant) <br>
- [WeChat authorization landing page](https://xiaomaxiangshenghuo.io.mlj130.com/authlogin.html) <br>
- [Rebate details page](https://xiaomaxiangshenghuo.io.mlj130.com/rebate-details.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown user-facing replies and JSON routing or search payloads emitted by Node.js CLI scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Script stdout is intended to be returned verbatim; supported script output formats include md and json.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
