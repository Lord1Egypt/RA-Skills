## Description: <br>
Guides agents to use the SYSU Anything CLI for SYSU campus services such as course schedules, leave requests, Rain Classroom tasks, check-ins, venue bookings, shuttle lookups, career events, campus Q&A, and CAS-based login recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qybaihe](https://clawhub.ai/user/qybaihe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External SYSU users and agents use this skill to route natural-language campus-service requests into safe SYSU Anything CLI commands, including login checks, previews, bookings, applications, reminders, and campus information lookups. <br>

### Deployment Geography for Use: <br>
China (SYSU campus services) <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated workflows can use locally stored SYSU campus session files and sensitive callback URLs. <br>
Mitigation: Use only trusted machines, do not share callback URLs, logs, or files from ~/.sysu-anything, and restore login state with the documented status and auth commands before running protected actions. <br>
Risk: Some campus workflows can submit leave requests, bookings, applications, or reservations when --confirm is used. <br>
Mitigation: Run help, query, and preview commands first; add --confirm only after the user explicitly asks to submit or finalize the action. <br>
Risk: Incorrect homework attachment paths or guessed IDs, venue names, callback URLs, or research identifiers could cause wrong submissions or data exposure. <br>
Mitigation: Double-check attachment paths and identifiers with the user, prefer --json when available, and avoid guessing values that the CLI can query. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qybaihe/sysu-anything-cli) <br>
- [SYSU-Anything repository linked by artifact README](https://github.com/qybaihe/SYSU-Anything) <br>
- [Skill definition](SKILL.md) <br>
- [Artifact README](README.md) <br>
- [Capability overview](references/overview.md) <br>
- [Authentication and local state](references/auth-and-state.md) <br>
- [Safety and confirmation boundaries](references/safety-and-confirm.md) <br>
- [Apple integration](references/apple.md) <br>
- [USC and BPM reservations](references/usc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON-producing CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Normal operation depends on the sysu-anything CLI and, for authenticated workflows, locally stored SYSU campus session files.] <br>

## Skill Version(s): <br>
0.3.6 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
