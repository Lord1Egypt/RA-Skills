## Description: <br>
Queries current meeting room status, including available rooms and recently released rooms, and formats the results for users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[naffan2014](https://clawhub.ai/user/naffan2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and workplace assistants use this skill to check which meeting rooms are currently available or were recently released. It presents room status in grouped Markdown tables and includes the booking portal link for follow-up reservation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Room status responses can include meeting-room availability and recently released-room booker names and subjects. <br>
Mitigation: Confirm that the smartrooms.ke.com service and displayed meeting metadata are appropriate for the organization before installation. <br>
Risk: The skill points users to an external booking portal after presenting query results. <br>
Mitigation: Confirm that https://new-meeting.ke.com/ is the approved booking destination for the intended users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/naffan2014/room-status-query) <br>
- [Meeting room status API host](https://smartrooms.ke.com) <br>
- [Meeting room booking portal](https://new-meeting.ke.com/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, guidance] <br>
**Output Format:** [Markdown tables with status text and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Groups results by city and office area; converts release times to Beijing time.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
