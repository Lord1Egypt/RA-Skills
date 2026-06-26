## Description: <br>
This skill helps agents browse, quote, purchase, and manage Snaplii gift cards and bill payments using a pre-funded Snaplii Cash balance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snapliiai](https://clawhub.ai/user/snapliiai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to browse eligible Snaplii gift cards and bill payees, preview cashback or voucher savings, and complete explicitly confirmed purchases or bill payments from a pre-funded Snaplii Cash balance. <br>

### Deployment Geography for Use: <br>
Canada and United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes gateway or base-url switching inside a financial workflow. <br>
Mitigation: Use gateway switching only when deliberately connecting to a trusted Snaplii environment. <br>
Risk: Purchases and bill payments can spend a user's pre-funded Snaplii Cash balance. <br>
Mitigation: Before execution, verify the amount, biller or brand, region, and that payment is coming only from Snaplii Cash. <br>
Risk: The workflow handles sensitive API keys and gift card redemption details. <br>
Mitigation: Enter API keys only through hidden CLI prompts and show redemption details only when the user explicitly requests them. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/snapliiai/snaplii-a2m-payment) <br>
- [Snaplii CLI on PyPI](https://pypi.org/project/snaplii-cli/) <br>
- [Snaplii app for iOS](https://apps.apple.com/app/snaplii/id1596924498) <br>
- [Snaplii app for Android](https://play.google.com/store/apps/details?id=com.snaplii.app) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and concise transaction summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes user-confirmed payment flows and defers sensitive redemption details until explicitly requested.] <br>

## Skill Version(s): <br>
1.11.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
