## Description: <br>
Jielong CLI helps agents manage Jielong activities through the jielong command-line tool, including creating, viewing, updating, deleting, and managing registrations and activity state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liu-tao-hash](https://clawhub.ai/user/liu-tao-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to have an agent manage Jielong signup, paid registration, and check-in activities through CLI commands. It supports activity creation, lookup, updates, signup management, state changes, and deletion workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install a global npm CLI, open a login QR flow, and run commands that change Jielong account data. <br>
Mitigation: Use it only in an environment where the user expects the jielong CLI to run, and require explicit user confirmation before login, creation, mutation, or deletion actions. <br>
Risk: Account details, phone numbers, OpenID values, activity IDs, and signup records may appear in command output. <br>
Mitigation: Avoid sharing command output outside the active session, redact personal identifiers when they are not needed, and confirm the account belongs to the user before continuing. <br>
Risk: Deletion, clearing signups, and state-change commands can be destructive or difficult to reverse. <br>
Mitigation: Confirm the target activity and requested action with the user before running destructive commands, and prefer listing or viewing records first to verify IDs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liu-tao-hash/skills/tianba-jielong) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute jielong CLI commands and prepare temporary JSON configuration for complex activity creation.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
