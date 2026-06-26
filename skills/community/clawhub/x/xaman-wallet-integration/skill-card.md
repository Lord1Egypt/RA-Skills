## Description: <br>
Integrate Xaman wallet (formerly Xumm) for XRP Ledger authentication and transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HarleysCodes](https://clawhub.ai/user/HarleysCodes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to add Xaman wallet connection, sign-in, session handling, and XRP Ledger payment or signature request flows to web applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet sessions and JWT persistence can expose user account state on shared or compromised devices. <br>
Mitigation: Configure API key origins and redirect URLs tightly, consider disabling persistent sessions or using custom storage for sensitive apps, and provide logout on shared devices. <br>
Risk: Payment or signature requests may be misused if users cannot clearly inspect what they are approving. <br>
Mitigation: Require clear user confirmation for every payment or signature request and harden the app against XSS before using the wallet flow. <br>
Risk: The integration depends on the external Xaman SDK source. <br>
Mitigation: Use the SDK only when the application owner trusts the Xaman SDK source and its operational availability. <br>


## Reference(s): <br>
- [Xaman Developer Dashboard](https://xumm.app/dashboard/developer) <br>
- [XummPkce SDK CDN](https://xumm.app/assets/cdn/xumm-oauth2-pkce.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with inline HTML and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [References NEXT_PUBLIC_XAMAN_API_KEY, redirect URL configuration, and Xaman SDK session options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
