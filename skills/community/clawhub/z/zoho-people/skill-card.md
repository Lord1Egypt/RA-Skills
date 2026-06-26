## Description: <br>
Zoho People API integration with managed OAuth for managing employees, departments, designations, attendance, leave, and arbitrary Zoho People forms, including custom forms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to Zoho People through Maton-managed OAuth and perform targeted HR record lookup, form access, attendance, leave, and approved write operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and change sensitive HR records through Maton when credentials are provided. <br>
Mitigation: Use the least-privileged Zoho connection available and only access specific records the user requests. <br>
Risk: Multiple Zoho People connections can route requests to the wrong account if no connection is specified. <br>
Mitigation: Specify the intended Maton connection when multiple accounts exist. <br>
Risk: Create, update, or delete operations can modify HR data. <br>
Mitigation: Review every write request with the target resource and intended effect before approving execution. <br>
Risk: Broad employee exports can expose personal HR data. <br>
Mitigation: Avoid bulk employee retrieval unless there is a clear user-requested need. <br>


## Reference(s): <br>
- [Zoho People API Overview](https://www.zoho.com/people/api/overview.html) <br>
- [Zoho People Fetch Forms API](https://www.zoho.com/people/api/forms-api/fetch-forms.html) <br>
- [Zoho People Get Bulk Records API](https://www.zoho.com/people/api/bulk-records.html) <br>
- [Zoho People Insert Records API](https://www.zoho.com/people/api/insert-records.html) <br>
- [Zoho People Update Records API](https://www.zoho.com/people/api/update-records.html) <br>
- [Zoho People Attendance API](https://www.zoho.com/people/api/attendance-entries.html) <br>
- [Zoho People Add Leave API](https://www.zoho.com/people/api/add-leave.html) <br>
- [Zoho People Skill Page](https://clawhub.ai/byungkyu/zoho-people) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May issue HTTP requests to Maton and Zoho People when the user provides credentials and approves write operations.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
