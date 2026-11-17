## Description:

Integrate Xaman wallet SDK to authenticate users, connect wallets, request XRP payments, and manage sessions on the XRP Ledger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harleyscodes](https://clawhub.ai/user/harleyscodes)

### License/Terms of Use:


## Use Case:

Developers use this skill to add Xaman/Xumm wallet connection, sign-in, session recovery, and XRP Ledger payment or signature request guidance to a web application.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet integration guidance can lead to unsafe session persistence or unclear transaction approval flows if copied without review.

Mitigation: Review SDK delivery and session storage choices, avoid unnecessary persistent browser sessions, and require users to verify transaction details in Xaman.

Risk: Loading the wallet SDK from an external CDN makes the application depend on third-party SDK delivery.

Mitigation: Review the SDK delivery method and vendor-provided SDK path before deployment.

## Reference(s):

- [XummPkce SDK CDN](https://xumm.app/assets/cdn/xumm-oauth2-pkce.min.js)
- [Xaman Developer Dashboard](https://xumm.app/dashboard/developer)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration]

**Output Format:** [Markdown with TypeScript and HTML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API key environment variable guidance and wallet-session handling notes.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
