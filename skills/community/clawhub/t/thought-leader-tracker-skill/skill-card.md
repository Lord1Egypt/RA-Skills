## Description: <br>
Thought Leader Tracker collects podcasts, interviews, and videos from configured thought leaders across YouTube, Apple Podcasts, and Spotify and generates Markdown digest reports with summaries, key points, and common themes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rickytsao-swordedge](https://clawhub.ai/user/rickytsao-swordedge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to maintain a configurable watchlist of thought leaders, collect recent podcast and video references, and produce daily Markdown digests for trend monitoring and content review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may be low quality or misattributed. <br>
Mitigation: Treat reports as rough search digests and verify links, publication dates, summaries, and attribution before relying on them. <br>
Risk: Configured thought-leader names and keywords are sent to Apple's public search API during collection. <br>
Mitigation: Avoid adding sensitive tracking terms and review config.json before manual, scheduled, or shared runs. <br>
Risk: Scheduled cron usage can create ongoing network activity and local report files. <br>
Mitigation: Enable scheduled runs only when ongoing daily collection is intended and periodically review generated reports. <br>
Risk: YouTube and Spotify collection require credentials and are placeholder paths without the documented API setup. <br>
Mitigation: Configure the relevant API credentials before expecting complete cross-platform coverage. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [ClawHub skill page](https://clawhub.ai/rickytsao-swordedge/thought-leader-tracker-skill) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes dated report files under daily-logs; collection window defaults to 7 days and can be set to 30 days.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, target metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
