## Description: <br>
Q Wms helps agents answer Qianyi WMS questions about warehouse status, to-dos, exceptions, backlog causes, issue follow-up, inventory, orders, tasks, performance, and warehouse or owner context through q-claw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ljqdh](https://clawhub.ai/user/ljqdh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Warehouse managers, supervisors, and operators use this skill to query Qianyi WMS data for daily warehouse overviews, exceptions, outbound backlog analysis, inventory, orders, tasks, and performance. It is intended for authenticated WMS lookups where the agent should ground business answers in current q-claw results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can query warehouse, inventory, order, task, performance, and exception data through q-claw. <br>
Mitigation: Install it only for intended Qianyi WMS users and use accounts with appropriate WMS permissions. <br>
Risk: Warehouse answers may be misleading if they are produced from examples, memory, or prior conversation instead of current WMS results. <br>
Mitigation: Ground business responses in the current q-claw result and ask for missing SKU, warehouse, or owner context when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ljqdh/q-wms) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Localized natural-language text with Markdown links when authorization is required] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Business results should be based on the current q-claw response; WMS authorization and account permissions may be required.] <br>

## Skill Version(s): <br>
1.0.73 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
