## Description:

Automates Shanghai Library East Branch third-floor seat workflows, including browser-assisted login, profile-based authentication refresh, availability checks, booking, listing, and cancellation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jenslewie](https://clawhub.ai/user/jenslewie)

### License/Terms of Use:

MIT-0

## Use Case:

External users with Shanghai Library reader access use this skill to manage East Branch third-floor seat reservations from an agent-guided CLI workflow. It is useful for checking common all-day availability, booking a specific or automatically assigned seat, listing active reservations, and canceling selected reservations.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill stores Shanghai Library authentication tokens in local profile files.

Mitigation: Keep profile files private, restrict filesystem permissions, and avoid committing or sharing profile directories.

Risk: Booking and cancellation commands can modify real seat reservations.

Mitigation: Review command arguments, especially reservation IDs and dates, before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jenslewie/skills/shlibrary-seat-booking)
- [OpenClaw Homepage](https://github.com/jenslewie/jenslewie-skills/tree/main/shlibrary-seat-booking)
- [API Reference](references/api_reference.md)
- [Shanghai Library Seat Reservation Site](https://yuyue.library.sh.cn)
- [Shanghai Library Seat Notice](https://yuyue.library.sh.cn/notice/seatAllNotice.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces user-directed CLI instructions and command outcomes for authentication, availability lookup, booking, listing, and cancellation.]

## Skill Version(s):

0.1.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
