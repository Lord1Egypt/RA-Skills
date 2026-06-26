## Description: <br>
Automatically distributes products from Kuairui's product catalog to the Ozon e-commerce platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[famechyu](https://clawhub.ai/user/famechyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce operators use this skill to collect category, store, and price range parameters, then run browser automation that publishes matching products to Ozon. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs live browser automation that can submit publishing actions. <br>
Mitigation: Review the selected category, store, and price range before execution, and use a version that requires explicit confirmation before sending. <br>
Risk: The automation uses hard-coded login credentials for the target service. <br>
Mitigation: Replace embedded credentials with user-managed credentials and limit account permissions to the minimum required for product publishing. <br>
Risk: The target service is a raw HTTP endpoint. <br>
Mitigation: Confirm that the service is trusted and reachable only in the intended environment before installing or running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/famechyu/test-publish) <br>
- [Automation target service](http://139.9.192.16:9089/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text task status with command execution logs and a screenshot file path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires category, store, and price range inputs before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
