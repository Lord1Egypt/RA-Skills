## Description: <br>
Operating doctrine for TikTok account automation with role separation, Business Suite DM and comment workflows, conservative quotas, account-safety checks, and recovery patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators, creators, agencies, and developers use this skill to configure and supervise scheduled TikTok brand-account activity across messages, comments, posting cadence, state tracking, and recovery workflows. It is intended for accounts where account safety and long-term reach matter more than raw automation volume. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring logged-in DM and comment automation can trigger platform enforcement, account loss, or reach throttling. <br>
Mitigation: Use the skill only on accounts you control, review workflows before scheduling them, keep quotas conservative, and stop automation after warnings or soft blocks. <br>
Risk: The workflow requires access to a logged-in browser profile and OS-level Accessibility or UI-control permissions. <br>
Mitigation: Run it from an isolated browser profile in a low-privilege environment, and revoke browser or Accessibility access when automation is not actively needed. <br>
Risk: Human-like UI control and anti-detection tactics increase platform-policy and account-safety sensitivity. <br>
Mitigation: Avoid unsolicited outbound DMs and comments, require human review for scheduled workflows, and prefer manual intervention for appeals, account warnings, and unusual UI changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexbloch-ia/tiktok-account-operations) <br>
- [Publisher profile](https://clawhub.ai/user/alexbloch-ia) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [TikTok Business Suite Messages](https://www.tiktok.com/business-suite/messages) <br>
- [TikTok Business Suite Comments](https://www.tiktok.com/business-suite/comments) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands] <br>
**Output Format:** [Markdown guidance with YAML configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes account-specific placeholders, schedules, quotas, state files, and recovery procedures; workflows should be reviewed before enabling automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
