## Description: <br>
Executes the pre-reconciliation workflow for Youxinpai monthly deposit reconciliation by checking local prerequisites, triggering related data warehouse tasks in the Xinghe task page, running the required SQL step, and reporting execution results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[just4learn1](https://clawhub.ai/user/just4learn1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authorized employees use this skill to run the pre-reconciliation steps for Youxinpai monthly deposit workflows, including local configuration checks, targeted task triggering, SQL execution, and concise status reporting. It supports operational preparation and exception reporting, not final financial reconciliation approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can modify local project files before running the reconciliation prerequisites. <br>
Mitigation: Confirm authorization, review the exact file changes, record the original configuration value, and restore the local configuration after execution. <br>
Risk: The workflow can trigger internal data jobs and run SQL through an existing corporate session. <br>
Mitigation: Require explicit approval before triggering tasks or SQL, confirm the target month and pages, and stop on permission, login, page, or SQL errors. <br>
Risk: The skill supports reconciliation preparation but does not provide final financial approval. <br>
Mitigation: Treat the output as an execution report and require human review for downstream reconciliation and finance decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/just4learn1/youxinpai-reconciliation) <br>
- [Xinghe task list](https://dp.58corp.com/data-develop/task-list) <br>
- [SQL query page](https://dp.58corp.com/data-query?doc_ids=530490) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown progress updates and result tables, with local commands or configuration details when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports task status, SQL execution status, exceptions, and whether local configuration was restored.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
