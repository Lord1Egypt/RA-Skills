## Description: <br>
Finds recently launched viral YouTube Shorts channels using criteria for channel age, total views, and average views, then returns qualifying channel links and stats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abdullahsarumi16-stack](https://clawhub.ai/user/abdullahsarumi16-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, researchers, and channel operators use this skill to identify new YouTube Shorts channels that meet viral-growth criteria and receive concise channel summaries for niche research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes automatic weekly Telegram delivery to a named recipient and heartbeat tracking without adequate user control. <br>
Mitigation: Remove or disable the weekly schedule, Telegram delivery, and heartbeat update unless the user explicitly approves that automation and recipient. <br>
Risk: The skill can repeatedly run local YouTube research until enough qualifying channels are found. <br>
Mitigation: Require explicit user approval before running the local script, and let the user set result limits before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abdullahsarumi16-stack/youtube-shorts-niche-research) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with YouTube links, channel handles, and performance stats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on a local research script and dated JSON result files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
