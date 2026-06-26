## Description: <br>
Scan Urban Sports Club venues, list courses with booking links, and book or cancel courses using USC login credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niklaspriddat](https://clawhub.ai/user/niklaspriddat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and personal automation users use this skill to scan configured Urban Sports Club venues, inspect upcoming classes, and manage bookings from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Urban Sports Club login credentials locally for booking-related commands. <br>
Mitigation: Keep credentials.json private, use an isolated environment, and avoid sharing the skill directory after credentials are added. <br>
Risk: Booking and cancellation commands can make real changes to a USC account. <br>
Mitigation: Double-check class IDs before running --book or --cancel and review command output after each account-changing action. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/niklaspriddat/usc-booking-api) <br>
- [Urban Sports Club](https://urbansportsclub.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI examples and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can perform user-directed booking, cancellation, and booking-list actions against an Urban Sports Club account.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
