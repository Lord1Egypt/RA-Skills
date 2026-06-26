## Description: <br>
Use ThreadPilot to manage Reddit account workflows from the CLI with human-in-the-loop safety and explicit confirmation before engagement actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vood](https://clawhub.ai/user/vood) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and external users use this skill to verify Reddit sessions, retrieve subreddit rules, inspect account activity, search or read Reddit content, and perform posting or engagement workflows with preview and confirmation gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run or bootstrap an external ThreadPilot binary. <br>
Mitigation: Review or manually install the ThreadPilot binary before first use, and install only when the upstream ThreadPilot code is trusted. <br>
Risk: The skill handles Reddit account actions and session-sensitive workflows. <br>
Mitigation: Use a test account or isolated environment when possible, and keep Reddit credentials and browser profiles scoped to the intended account. <br>
Risk: Posting, commenting, or liking can create public engagement from a Reddit account. <br>
Mitigation: Require dry-run previews and explicit confirmation before every like, comment, or post. <br>
Risk: Duplicate or rule-violating comments could be submitted if safeguards are bypassed. <br>
Mitigation: Keep duplicate-post protection enabled and retrieve subreddit rules before drafting or publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vood/reddit-skill) <br>
- [ThreadPilot binary reference](bin/REFERENCE.md) <br>
- [ThreadPilot repository](https://github.com/vood/threadpilot) <br>
- [ThreadPilot releases](https://github.com/vood/threadpilot/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and environment variables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run previews, explicit confirmation prompts, Reddit workflow commands, and configuration guidance for ThreadPilot.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
