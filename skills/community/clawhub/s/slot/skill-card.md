## Description: <br>
Use when managing time slots, creating schedule blocks, detecting booking conflicts, exporting calendars, or applying scheduling templates for appointments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use Slot to create, list, check, and export local schedule blocks for appointments, focus time, meetings, and reusable scheduling templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local schedule labels, categories, and exported calendar files may reveal sensitive availability or appointment details on shared or synced machines. <br>
Mitigation: Avoid sensitive labels, store data in a protected SLOT_DATA_DIR when needed, and restrict or delete local files after use. <br>
Risk: The create command can save a slot even after reporting a conflict, which may leave overlapping bookings in the local schedule. <br>
Mitigation: Run check-conflict before creating important slots and review conflict warnings before relying on exported calendars. <br>


## Reference(s): <br>
- [Slot on ClawHub](https://clawhub.ai/xueyetianya/slot) <br>
- [BytesAgain](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Plain text command output with optional CSV and iCal export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores schedule data locally under ~/.slot-manager unless SLOT_DATA_DIR is set.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
