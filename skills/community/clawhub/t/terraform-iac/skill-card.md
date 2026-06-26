## Description: <br>
Deep Terraform/IaC workflow\u2014module boundaries, state, workspaces, plan/apply safety, drift, secrets, CI integration, and team governance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawkk](https://clawhub.ai/user/clawkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to plan and review Terraform or related IaC work, including module design, state boundaries, secrets handling, CI plan/apply workflows, and drift recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Terraform guidance could be mistaken for approval to apply infrastructure changes automatically. <br>
Mitigation: Keep production applies behind human review, protected CI workflows, least-privilege cloud credentials, and rollback planning. <br>
Risk: Incorrect IaC advice could lead to destructive changes or state drift if applied without review. <br>
Mitigation: Require reviewed plans, documented state ownership, drift checks, and recovery procedures before applying changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/clawkk/terraform-iac) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with checklists and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces advisory workflow steps only; it does not run commands or apply infrastructure changes automatically.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
