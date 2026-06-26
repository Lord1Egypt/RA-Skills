## Description: <br>
Helps agents route SYSU campus workflows on macOS 12+ through the published sysu-anything-apple runtime so Calendar and Reminders items can be created for timetables, homework, reservations, career events, leave, and work-study tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qybaihe](https://clawhub.ai/user/qybaihe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, staff, and agent operators working with SYSU services use this skill to turn campus tasks into Apple Calendar events and Apple Reminders on supported macOS hosts. The skill guides command selection, login checks, preview behavior, and confirmation-gated writes for SYSU workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The runtime can write to Apple Calendar and Reminders and uses SYSU session data stored under ~/.sysu-anything. <br>
Mitigation: Install only when the sysu-anything npm package is trusted, run apple doctor before sync, and confirm the relevant SYSU login state before executing write workflows. <br>
Risk: Confirmation-gated commands can submit bookings, signups, leave requests, or other campus-service changes. <br>
Mitigation: Review generated commands before allowing any --confirm action; use preview or detail commands for local Calendar and Reminders import when remote submission is not intended. <br>
Risk: Apple sync is only supported on macOS 12+ and should not proceed when the native bridge or permissions are unavailable. <br>
Mitigation: Run sysu-anything-apple apple doctor first and fall back to sysu-anything without the Apple sync layer on unsupported hosts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qybaihe/sysu-anything-apple) <br>
- [SYSU-Anything repository](https://github.com/qybaihe/SYSU-Anything) <br>
- [SYSU anything Apple overview](references/overview.md) <br>
- [Career Apple integration](references/career.md) <br>
- [Libic Apple integration](references/libic.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend JSON output from the underlying CLI when another agent or script needs structured results.] <br>

## Skill Version(s): <br>
0.3.6 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
