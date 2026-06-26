## Description: <br>
Use the ZapYeti API to list debts, track balances, view payoff schedules, log payments, and monitor debt-free progress via api.zapyeti.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djedi](https://clawhub.ai/user/djedi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to query and manage ZapYeti debt payoff data through the ZapYeti REST API, including debts, balances, payments, payoff schedules, exports, SimpleFin sync, social features, and admin endpoints when authorized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access broad financial-account actions, including payments, exports, SimpleFin connections, social posting, API key management, account deletion, and admin endpoints. <br>
Mitigation: Use a least-privilege ZapYeti API key and require explicit user approval before any mutating, export, account, SimpleFin, social, API-key, or admin operation. <br>
Risk: Read-only debt and payment lookups may expose sensitive financial information. <br>
Mitigation: Install only when ZapYeti is trusted for the workflow and avoid sharing returned financial data beyond the user's requested task. <br>


## Reference(s): <br>
- [ZapYeti API reference](references/api.md) <br>
- [ZapYeti homepage](https://zapyeti.com) <br>
- [ZapYeti source link from metadata](https://github.com/djedi/zapyeti) <br>
- [ClawHub skill page](https://clawhub.ai/djedi/zapyeti) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, python3, and ZAPYETI_API_KEY. Amounts are represented in cents.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
