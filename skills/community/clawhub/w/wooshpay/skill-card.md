## Description: <br>
WooshPay API helps agents create payment intents, create hosted checkout sessions, query payment status, and process refunds using the WOOSHPAY_API_KEY environment variable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wp-ai-dev](https://clawhub.ai/user/wp-ai-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and payment operations teams use this skill to manage WooshPay payment flows from an agent workspace, including checkout creation, payment lookup, and refunds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A merchant WooshPay API key could be exposed through unsafe URL handling or poor secret guidance. <br>
Mitigation: Use a restricted WooshPay key where possible, store it in an environment variable or secret manager, and do not paste the key into chat. <br>
Risk: Payment and refund operations can move money or affect customer orders if run with incorrect inputs. <br>
Mitigation: Review each payment, checkout, order lookup, or refund before confirming, and do not pass full URLs to the order lookup script. <br>


## Reference(s): <br>
- [WooshPay Getting Started](https://docs.wooshpay.com/3647644m0) <br>
- [WooshPay Payment Methods](https://docs.wooshpay.com/3948703m0) <br>
- [WooshPay Supported Currencies](https://docs.wooshpay.com/2447438m0) <br>
- [ClawHub Skill Page](https://clawhub.ai/wp-ai-dev/wooshpay) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python script-driven WooshPay API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interactive scripts may print payment URLs, checkout session details, order status, refund results, and error responses.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
