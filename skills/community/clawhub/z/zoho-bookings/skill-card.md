## Description: <br>
Zoho Bookings API integration with managed OAuth for managing appointments, services, staff, and workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and operations teams use this skill to query Zoho Bookings data and perform user-approved booking, service, staff, workspace, and connection actions through Maton-managed OAuth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive Maton API key and managed OAuth access to Zoho Bookings. <br>
Mitigation: Keep MATON_API_KEY private, avoid sharing outputs that expose credentials, and install only when Maton is trusted to proxy Zoho Bookings access. <br>
Risk: Booking, service, workspace, staff, and connection write operations can change live scheduling data. <br>
Mitigation: Review the target resource, intended account connection, and requested create, update, or delete effect before approving any write operation. <br>
Risk: Multiple Maton connections may route requests to the wrong Zoho Bookings account if the connection is ambiguous. <br>
Mitigation: Specify the intended Maton-Connection header when multiple active connections exist. <br>


## Reference(s): <br>
- [ClawHub Zoho Bookings Skill](https://clawhub.ai/byungkyu/zoho-bookings) <br>
- [Maton](https://maton.ai) <br>
- [Zoho Bookings API Documentation](https://www.zoho.com/bookings/help/api/v1/oauthauthentication.html) <br>
- [Book Appointment API](https://www.zoho.com/bookings/help/api/v1/book-appointment.html) <br>
- [Fetch Appointments API](https://www.zoho.com/bookings/help/api/v1/fetch-appointment.html) <br>
- [Fetch Services API](https://www.zoho.com/bookings/help/api/v1/fetch-services.html) <br>
- [Fetch Staff API](https://www.zoho.com/bookings/help/api/v1/fetch-staff.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline Python, JavaScript, shell commands, HTTP endpoints, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, a MATON_API_KEY, and a connected Zoho Bookings OAuth account.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
