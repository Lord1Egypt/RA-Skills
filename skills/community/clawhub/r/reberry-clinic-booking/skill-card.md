## Description: <br>
Reberry helps users view booking guidance, submit appointment requests, consult customer service, and check prices for reberry医院 明洞店 through BeautsGO. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beautsgo](https://clawhub.ai/user/beautsgo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to book or prepare bookings for reberry clinic Myeongdong through BeautsGO, including viewing guidance, opening clinic pages, checking prices, and submitting appointment details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Appointment time, party size, and any phone number the user provides may be sent to BeautsGO when requesting a booking. <br>
Mitigation: Use the booking flow only after confirming the user is comfortable sharing those details with BeautsGO. <br>
Risk: The skill may submit a booking request once enough appointment information is present. <br>
Mitigation: Review the clinic, appointment details, and contact information before asking the skill to book. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/beautsgo/reberry-clinic-booking) <br>
- [BeautsGO publisher profile](https://clawhub.ai/user/beautsgo) <br>
- [reberry clinic Myeongdong page](https://i.beautsgo.com/cn/hospital/reberry-clinic-myeongdong?from=skill) <br>
- [reberry clinic Myeongdong booking page](https://i.beautsgo.com/cn/hospital/reberry-clinic-myeongdong/skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [String, often formatted as Markdown booking guidance or booking and price query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports Chinese and English responses; may return links to BeautsGO pages.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
