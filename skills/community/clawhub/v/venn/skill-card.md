## Description: <br>
Venn lets agents search, describe, and execute connected enterprise tools such as Jira, Salesforce, Gmail, Slack, Google Workspace, GitHub, Notion, and Box through the Venn tool-router API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neil-bd](https://clawhub.ai/user/neil-bd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and agents use this skill to discover connected enterprise SaaS tools, read business data, and prepare approved create, update, delete, or multi-step workflows across connected apps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access broad connected enterprise app data through Venn. <br>
Mitigation: Install only when Venn is trusted for the connected apps and use a least-privilege Venn API key. <br>
Risk: A shared sandbox image or configuration could expose the VENN_API_KEY. <br>
Mitigation: Store the key in a private environment or secrets helper and avoid placing it in shared sandbox images. <br>
Risk: Send, create, update, delete, or multi-step workflows can change enterprise records. <br>
Mitigation: Review the proposed operation carefully and require explicit user approval before confirming write or delete actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/neil-bd/venn) <br>
- [Venn API Keys](https://app.venn.ai/api-keys) <br>
- [Venn Tool Router API](https://app.venn.ai/api/tooliq) <br>
- [Platform Query Syntax](references/query-syntax.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VENN_API_KEY; write and delete operations require explicit user approval.] <br>

## Skill Version(s): <br>
2.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
