## Description: <br>
Revolut web automation via Playwright: login/logout, list accounts, and fetch transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to automate Revolut web banking workflows, including login, account balance retrieval, wallet transactions, investment portfolio holdings, and investment transactions. It is intended for private trusted workspaces because it handles banking session state and financial records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles banking login material and reusable browser session state. <br>
Mitigation: Install only in a private, trusted workspace, keep the revolut workspace directory out of sync, backup, and source control, and run logout after use to remove stored session data. <br>
Risk: A Revolut PIN may be stored in config.json for automated entry. <br>
Mitigation: Leave the PIN out of config.json unless the user explicitly accepts that risk and can protect the workspace file. <br>
Risk: Generated JSON and debug outputs may contain sensitive financial records. <br>
Mitigation: Treat account, transaction, portfolio, QR-code, and debug artifacts as sensitive data and avoid sharing or committing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/odrobnik/revolut) <br>
- [Skill homepage](https://github.com/odrobnik/revolut-skill) <br>
- [Setup guide](SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON files and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include account, transaction, portfolio, QR-code, and debug artifacts that should be treated as sensitive financial data.] <br>

## Skill Version(s): <br>
1.3.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
