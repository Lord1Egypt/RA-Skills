## Description: <br>
Automates Shanghai Library East Branch 3F seat workflows, including browser-assisted login, availability checks, seat booking, reservation listing, and cancellation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jenslewie](https://clawhub.ai/user/jenslewie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with Shanghai Library reader accounts use this skill to manage East Branch 3F seat reservations from an agent-assisted command workflow. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Shanghai Library session tokens in local profile JSON files. <br>
Mitigation: Protect profile files, do not commit or share them, and use restrictive local file permissions. <br>
Risk: Booking and cancellation commands directly change library reservations. <br>
Mitigation: Double-check the selected profile, date, seat details, and reservation ID before running book or cancel commands. <br>
Risk: Browser-assisted login requires installing Playwright and Chromium. <br>
Mitigation: Install dependencies from trusted package sources and review the local environment before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jenslewie/shlibrary-seat-booking) <br>
- [Project homepage](https://github.com/jenslewie/jenslewie-skills/tree/main/shlibrary-seat-booking) <br>
- [API reference](references/api_reference.md) <br>
- [Shanghai Library seat reservation rules](https://yuyue.library.sh.cn/notice/seatAllNotice.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may read or write local profile JSON files and call Shanghai Library reservation APIs.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
