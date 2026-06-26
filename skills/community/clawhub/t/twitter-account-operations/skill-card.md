## Description: <br>
Operating doctrine for X/Twitter account automation: stable Chrome sessions, role separation, human-like interaction, careful posting, reply discipline, and recovery patterns for scheduled account activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and account operators use this skill to guide scheduled X/Twitter posting, engagement, monitoring, metrics review, and recovery workflows while reducing account-safety and reputational risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent operating a real X/Twitter account, where posts, replies, likes, follows, or DMs may create reputational, compliance, or platform-policy exposure. <br>
Mitigation: Keep human review for public actions, use the role separation and read-before-acting checks, and stop rather than publish when the account cockpit or source evidence is uncertain. <br>
Risk: Browser profiles, account sessions, and webhook URLs used by scheduled automation may be sensitive. <br>
Mitigation: Use a dedicated browser profile, protect webhook URLs and local workspace files, and limit access to account automation credentials. <br>
Risk: Scheduled automation may conflict with X/Twitter platform rules, legal obligations, or brand policy if it runs without supervision. <br>
Mitigation: Confirm scheduled activity against current platform rules and organizational policy before enabling cron jobs, and keep manual review for suspensions or other account enforcement events. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/alexbloch-ia/twitter-account-operations) <br>
- [Publisher profile](https://clawhub.ai/user/alexbloch-ia) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Claude Code](https://claude.ai/code) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with YAML configuration examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes placeholder-based account, browser, schedule, workspace, and webhook settings for local adaptation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; release changelog text mentions v1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
