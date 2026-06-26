## Description: <br>
Generates and delivers a concise Rootly morning incident digest for on-call operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanibu2777](https://clawhub.ai/user/yanibu2777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations engineers and on-call responders use this skill to produce a daily Rootly briefing covering active incidents, recently resolved incidents, current on-call assignments, and overdue action items. It can support manual checks or scheduled Slack delivery through OpenClaw cron. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Slack digests can expose sensitive incident and on-call details if sent to the wrong channel. <br>
Mitigation: Verify the destination and cron schedule before enabling announcements, and send briefs only to restricted operations channels. <br>
Risk: Live Rootly access uses an API key that may expose incident data beyond the intended audience. <br>
Mitigation: Use a least-privilege Rootly key, store it in a protected secret file or environment variable, and rotate it according to internal policy. <br>
Risk: Private incident data may be included when explicitly enabled. <br>
Mitigation: Leave private incidents disabled by default and enable them only for approved recipients. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yanibu2777/rootly-morning-brief) <br>
- [README](README.md) <br>
- [Sample output](sample-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Slack-friendly plain text digest with optional JSON output and Markdown setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to public-only incidents, three items per section, and America/Toronto timezone; private incidents require explicit opt-in.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
