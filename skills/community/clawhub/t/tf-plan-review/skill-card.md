## Description: <br>
Analyze Terraform plans for risk before you apply, classify every change as safe, moderate, dangerous, or critical, and detect destroys, IAM changes, data-loss risks, and blast radius while never running apply. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tkuehnl](https://clawhub.ai/user/tkuehnl) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to review Terraform or OpenTofu plans, inspect state, validate configuration, and decide what needs human review before apply. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs Terraform or OpenTofu in a user-selected directory, which may contact provider APIs, registries, and state backends. <br>
Mitigation: Use a trusted Terraform directory, review providers and modules first, and run with least-privilege or read-only cloud credentials. <br>
Risk: Read-only and no-cache claims do not fully match temporary plan-file handling and local initialization behavior. <br>
Mitigation: Assume plan metadata may briefly touch local disk, run in a controlled workspace, and remove generated Terraform working files when appropriate. <br>
Risk: Plan and state context can expose sensitive infrastructure structure even when secret values are not extracted. <br>
Mitigation: Avoid sharing reports outside the authorized team and review high-risk changes with infrastructure or security owners before applying. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tkuehnl/tf-plan-review) <br>
- [Terraform install documentation](https://developer.hashicorp.com/terraform/install) <br>
- [OpenTofu install documentation](https://opentofu.org/docs/intro/install/) <br>
- [jq download documentation](https://jqlang.github.io/jq/download/) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, json, shell commands, guidance] <br>
**Output Format:** [Structured JSON for agent use and Markdown risk reports for human review.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Classifies Terraform or OpenTofu changes by risk level and highlights destructive, security-sensitive, drift, and pre-apply review items.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata; artifact frontmatter, changelog, and script report 0.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
