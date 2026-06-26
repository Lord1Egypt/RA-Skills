## Description: <br>
Twenty CRM API integration with managed authentication for managing companies, people, opportunities, notes, tasks, and workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to query and manage Twenty CRM records through Maton-managed authentication. It is suited for CRM workflows involving contacts, companies, deals, activities, and workspace tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Maton API key and can access connected Twenty CRM data. <br>
Mitigation: Install only if Maton is trusted with the target CRM data, keep MATON_API_KEY private, and limit use to intended connected workspaces. <br>
Risk: Write or delete operations can modify live CRM records and workflows. <br>
Mitigation: Confirm the exact record or connection ID and intended effect before create, update, or delete requests. <br>
Risk: Multiple Twenty connections can cause requests to target the wrong account. <br>
Mitigation: Use the Maton-Connection header when multiple accounts or workspaces are available. <br>


## Reference(s): <br>
- [ClawHub Twenty CRM Skill](https://clawhub.ai/byungkyu/twenty) <br>
- [Maton Homepage](https://maton.ai) <br>
- [Twenty API Documentation](https://twenty.com/developers/rest-api) <br>
- [Twenty GitHub](https://github.com/twentyhq/twenty) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions, API Calls] <br>
**Output Format:** [Markdown with inline Python, JavaScript, shell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY; responses depend on the connected Twenty CRM workspace.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
