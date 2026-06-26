## Description: <br>
Filters Feishu Bitable records with user-provided rules, sends formatted public-opinion alerts to a Feishu group webhook, and updates push-status fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankieway](https://clawhub.ai/user/frankieway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations, marketing, or customer-experience teams can use this skill to monitor Feishu Bitable public-opinion records, apply their own alert rules, and push selected results to a Feishu group for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill evaluates user-provided Python rule expressions against Feishu table data. <br>
Mitigation: Install only for trusted publishers and allow only trusted operators to provide or change rule expressions before execution. <br>
Risk: The skill sends selected table fields to a user-supplied Feishu webhook, which can expose sensitive records if configured broadly. <br>
Mitigation: Use a narrowly scoped Feishu app, send only non-sensitive fields, and point the webhook to a Feishu group controlled by the deploying team. <br>
Risk: The security summary flags possible unexpected resends and review needs around the duplicate execution path and dependency pinning. <br>
Mitigation: Review and fix the duplicate execution path, validate idempotent status updates in a limited view, and pin dependencies before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frankieway/yuqing-push-skill) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, configuration] <br>
**Output Format:** [Plain text status output plus Feishu webhook message payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns pushed_count, sends selected records to the configured Feishu webhook, and updates the Feishu Bitable push status field.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
