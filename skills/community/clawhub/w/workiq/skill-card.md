## Description: <br>
Query Microsoft 365 data, including emails, meetings, documents, Teams messages, and people, using the WorkIQ CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[likudo95](https://clawhub.ai/user/likudo95) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and agents use this skill to answer questions about Microsoft 365 content available to the signed-in account, including email, calendar, documents, Teams messages, people/org information, and meeting notes. It is intended for permission-scoped retrieval and summarization, not for granting additional access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries can expose Microsoft 365 content that the signed-in account is authorized to access, including sensitive legal, HR, medical, financial, or confidential project data. <br>
Mitigation: Use narrow prompts, avoid broad searches over sensitive data unless intended, and review returned content before reuse. <br>
Risk: The skill depends on the WorkIQ CLI or npm package and the selected Entra tenant. <br>
Mitigation: Verify the WorkIQ CLI/package and intended tenant before use, and complete EULA or sign-in steps deliberately. <br>


## Reference(s): <br>
- [Microsoft WorkIQ overview](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/workiq-overview) <br>
- [ClawHub WorkIQ skill page](https://clawhub.ai/likudo95/workiq) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, text] <br>
**Output Format:** [Markdown with inline shell commands and natural-language CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs standalone WorkIQ CLI queries; do not pipe or combine WorkIQ output with other shell commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
