## Description: <br>
Monitors selected official video channels for new non-Shorts videos from the past week and produces linked update reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FredHNian](https://clawhub.ai/user/FredHNian) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing, competitive intelligence, and content teams use this skill to track official brand video channels and summarize recent long-form uploads across a maintained channel list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The channel-list filename is inconsistent across the skill instructions. <br>
Mitigation: Confirm the intended channel-list path before using or updating the monitored channel configuration. <br>
Risk: Browsing logged-in YouTube pages may expose account-context content to the agent. <br>
Mitigation: Use a browser/session context appropriate for the channels being checked and avoid logged-in browsing unless that account context is acceptable. <br>
Risk: Video availability, counts, and regional visibility can vary by platform, account state, and location. <br>
Mitigation: Treat generated reports as current observations and verify important findings against the source channel before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FredHNian/video-channels-update-push) <br>
- [Tracked video channel list](artifact/video-channels.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown report with linked video entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include channel name, video title, duration, publish date, view count, and a view-level star rating.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
