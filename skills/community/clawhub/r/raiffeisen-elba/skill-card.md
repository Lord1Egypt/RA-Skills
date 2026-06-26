## Description: <br>
Automate Raiffeisen ELBA online banking: login/logout, list accounts, and fetch transactions via Playwright. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and automation agents use this skill to retrieve Raiffeisen ELBA account balances, securities depot positions, transactions, and related banking records for personal finance workflows. <br>

### Deployment Geography for Use: <br>
Global, for users with access to Raiffeisen ELBA online banking. <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles an ELBA PIN, browser session state, bearer token, transactions, portfolio data, and potentially bank documents. <br>
Mitigation: Run it only in a private, trusted workspace, keep credential and session files private, and review the skill before use with real banking credentials. <br>
Risk: Helper scripts can collect and download sensitive banking documents to local storage. <br>
Mitigation: Use document collection or download helpers only when intentional, store outputs in approved locations, and delete exported records that are no longer needed. <br>
Risk: The automation extracts a bearer token from the authenticated browser context to reuse the bank session. <br>
Mitigation: Complete 2FA only for expected login attempts, run logout after operations, and clear session artifacts if any command fails or behaves unexpectedly. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/odrobnik/raiffeisen-elba) <br>
- [Security policy](SECURITY.md) <br>
- [Setup instructions](SETUP.md) <br>
- [Accounts output schema](references/accounts.schema.json) <br>
- [Transactions output schema](references/transactions.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, CSV, Files] <br>
**Output Format:** [Markdown instructions with bash commands; executed scripts can emit JSON, CSV, and downloaded local files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Python dependencies, a config.json credential file, and manual pushTAN approval for login.] <br>

## Skill Version(s): <br>
1.4.4 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
