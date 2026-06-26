## Description: <br>
Zoho Projects API V3 integration with managed OAuth for managing projects, tasks, milestones, tasklists, users, comments, and team collaboration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an authorized Zoho Projects account through Maton-managed OAuth, inspect project data, and prepare or execute approved project, task, milestone, tasklist, comment, and user API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Zoho Projects data through a Maton-managed OAuth connection. <br>
Mitigation: Connect only the intended Zoho account and use the Maton-Connection header when more than one connection exists. <br>
Risk: Create, update, and delete calls can change project data. <br>
Mitigation: Review the target resource and intended effect before approving any POST, PATCH, or DELETE request. <br>
Risk: MATON_API_KEY is a sensitive credential. <br>
Mitigation: Keep the API key out of logs, shared terminal output, and committed files. <br>


## Reference(s): <br>
- [Zoho Projects on ClawHub](https://clawhub.ai/byungkyu/zoho-projects) <br>
- [byungkyu publisher profile](https://clawhub.ai/user/byungkyu) <br>
- [Maton](https://maton.ai) <br>
- [Zoho Projects API V3 Documentation](https://projects.zoho.com/api-docs) <br>
- [Zoho Projects Developer Portal](https://www.zoho.com/projects/help/rest-api/zohoprojectsapi.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline HTTP endpoints and Python, JavaScript, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and user-authorized Zoho Projects OAuth connection.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
