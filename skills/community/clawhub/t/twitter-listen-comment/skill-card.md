## Description: <br>
Monitor one or more Twitter/X usernames via the 6551 API, generate a short humorous reply with `openclaw agent --json`, and submit the reply through an already logged-in Chrome X session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yugulugulu](https://clawhub.ai/user/yugulugulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to watch selected Twitter/X accounts, generate short replies, submit comments through a logged-in browser session, and send notification messages about detected tweets and submitted comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish replies from a logged-in Twitter/X account without a clear manual approval or dry-run gate. <br>
Mitigation: Use a test account first, verify watched users and notification targets, review external data flows, and require manual approval or dry-run mode before live posting. <br>
Risk: Browser-driven posting depends on Chrome login state, Chrome Relay availability, and the current Twitter/X page state. <br>
Mitigation: Confirm the browser session and relay connection before running, and monitor the generated notification and log output for failed or incomplete submissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yugulugulu/twitter-listen-comment) <br>
- [Config reference](references/config.md) <br>
- [Example configuration](references/config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runtime automation can send notifications and attempt browser-driven Twitter/X comments from the logged-in account.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
