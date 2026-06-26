## Description: <br>
Avoid common Terraform mistakes - state corruption, count vs for_each, lifecycle traps, and dependency ordering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill for Terraform best-practice guidance when managing state, dependencies, modules, variables, imports, and lifecycle behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Terraform changes can modify or destroy real infrastructure resources when users act on generated guidance or commands. <br>
Mitigation: Review generated Terraform configuration and command plans before running terraform apply, destroy, import, state, or other mutating commands. <br>
Risk: Terraform state can contain secrets and can be corrupted or exposed if handled casually. <br>
Mitigation: Use remote encrypted state with locking, restrict access to state storage, and use Terraform state commands instead of manual state edits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/terraform) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline Terraform and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the terraform binary when advice is acted on locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
