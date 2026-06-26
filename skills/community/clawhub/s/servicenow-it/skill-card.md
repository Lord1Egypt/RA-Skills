## Description: <br>
ServiceNow IT Service Management integration with API key authentication. Manage incidents, problems, change requests, tasks, CMDB records, service catalog items, and IT operations via the ServiceNow REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, IT operators, and service desk teams use this skill to connect an agent to ServiceNow through ClawLink and manage ITSM workflows such as incidents, change requests, CMDB records, catalog orders, attachments, and tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary reports that the Quick Start includes unrelated SendGrid write commands that could modify the wrong connected account. <br>
Mitigation: Do not run the Quick Start commands as written; verify ServiceNow connectivity with read-only ServiceNow discovery commands before any write operation. <br>
Risk: ServiceNow write operations can create, update, delete, check out, attach files to, or modify CMDB records and service catalog requests. <br>
Mitigation: Require explicit user confirmation after reviewing the target resource, parameters, and preview for every create, update, delete, checkout, attachment, or CMDB operation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/servicenow-it) <br>
- [ServiceNow REST API Documentation](https://docs.servicenow.com/category/nav_to_landing_page) <br>
- [ServiceNow Table API](https://docs.servicenow.com/en-US/docs/services/rest-table) <br>
- [ServiceNow Change Management](https://docs.servicenow.com/category/change-management) <br>
- [ServiceNow CMDB](https://docs.servicenow.com/category/configuration-management) <br>
- [ServiceNow Service Catalog](https://docs.servicenow.com/category/service-catalog) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected ServiceNow account through ClawLink; write operations should be previewed and explicitly confirmed.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
