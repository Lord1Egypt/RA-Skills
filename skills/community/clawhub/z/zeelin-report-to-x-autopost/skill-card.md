## Description: <br>
Automatically selects the latest unposted report from a website or JSON feed, drafts an English X/Twitter post, publishes it through a logged-in X web session, records posted reports to avoid duplicates, and can be scheduled with OpenClaw cron. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelcey2023](https://clawhub.ai/user/kelcey2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate recurring report promotion on X while avoiding duplicate posts through a local posted-state file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish public X posts and set up recurring automation. <br>
Mitigation: Use only with an X account intended for automation, preview the generated post, and require explicit approval before first posting or cron setup. <br>
Risk: The helper script may update its posted-state file even when the posting helper fails. <br>
Mitigation: Confirm posting success before writing the report id to state so failed attempts can be retried. <br>
Risk: The workflow depends on a separate tweet.sh helper and an active logged-in web session. <br>
Mitigation: Inspect the helper before use and run it in a contained environment with the intended browser session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kelcey2023/zeelin-report-to-x-autopost) <br>
- [Report source website](https://thu-nmrc.github.io/THU-ZeeLin-Reports/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and a Python helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in X web session, a configured report source, local posted-state storage, and explicit approval before posting or scheduling.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
