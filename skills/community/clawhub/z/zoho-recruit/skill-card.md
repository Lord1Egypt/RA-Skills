## Description: <br>
Zoho Recruit API integration with managed OAuth for reading, creating, updating, searching, and deleting candidates, job openings, interviews, applications, and related recruiting workflow records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and recruiting operations teams use this skill to connect an agent to Zoho Recruit through Maton-managed OAuth, inspect recruiting records, and perform approved candidate, job opening, interview, application, and workflow updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, and delete Zoho Recruit records in a connected recruiting account. <br>
Mitigation: Require a clear preview of target records and intended effects before approving create, update, delete, or connection-management actions. <br>
Risk: The MATON_API_KEY and OAuth connection can grant access to sensitive recruiting data. <br>
Mitigation: Keep MATON_API_KEY secret and use the least-privileged Zoho or Maton connection available. <br>
Risk: Requests may be sent to the wrong Zoho Recruit account when multiple connections exist. <br>
Mitigation: Specify the Maton-Connection header whenever more than one active connection is available. <br>


## Reference(s): <br>
- [Zoho Recruit ClawHub Listing](https://clawhub.ai/byungkyu/zoho-recruit) <br>
- [Zoho Recruit API v2 Overview](https://www.zoho.com/recruit/developer-guide/apiv2/) <br>
- [Zoho Recruit Get Records API](https://www.zoho.com/recruit/developer-guide/apiv2/get-records.html) <br>
- [Zoho Recruit Insert Records API](https://www.zoho.com/recruit/developer-guide/apiv2/insert-records.html) <br>
- [Zoho Recruit Update Records API](https://www.zoho.com/recruit/developer-guide/apiv2/update-records.html) <br>
- [Zoho Recruit Delete Records API](https://www.zoho.com/recruit/developer-guide/apiv2/delete-records.html) <br>
- [Zoho Recruit Search Records API](https://www.zoho.com/recruit/developer-guide/apiv2/search-records.html) <br>
- [Zoho Recruit Modules API](https://www.zoho.com/recruit/developer-guide/apiv2/modules-api.html) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with Python and HTTP examples that return JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a valid Zoho Recruit OAuth connection; write operations require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
