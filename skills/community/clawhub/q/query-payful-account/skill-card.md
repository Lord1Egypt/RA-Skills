## Description: <br>
Queries Payful account information including balances, transactions, and account details using PAYFUL_TOKEN and PAYFUL_USER_ID environment variables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hugogu](https://clawhub.ai/user/hugogu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Payful account status and balance information for an authenticated Payful account. It is intended for trusted local environments where full Payful session-cookie credentials can be handled safely. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses full Payful browser-session cookies that can grant account access if exposed. <br>
Mitigation: Run only in trusted local environments, keep PAYFUL_TOKEN and PAYFUL_USER_ID secret, and rotate or invalidate them if exposed. <br>
Risk: The custom --api-url option can send Payful credentials to a user-supplied endpoint. <br>
Mitigation: Use the default Payful endpoint unless the alternate HTTPS endpoint has been verified as official. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hugogu/query-payful-account) <br>
- [Payful account balance endpoint](https://global.payful.com/api/user/account/queryUserAccBalByHomePage) <br>
- [Payful global site](https://global.payful.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands] <br>
**Output Format:** [Plain text balance summary, normalized JSON account list, or raw API JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PAYFUL_TOKEN and PAYFUL_USER_ID; supports an optional custom API base URL.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
