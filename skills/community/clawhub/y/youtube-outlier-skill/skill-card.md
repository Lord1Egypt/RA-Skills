## Description: <br>
Finds trending YouTube outlier videos by niche, analyzes key concepts, saves data to Google Sheets, and posts summaries to Discord. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dalime](https://clawhub.ai/user/dalime) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators, researchers, and channel operators use this skill to identify recent YouTube videos that substantially outperform peers for one or more niches, then route the findings into Google Sheets and Discord for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends YouTube research results to configured Google Sheets and Discord destinations. <br>
Mitigation: Use a least-privilege Google service account, restrict the Discord bot to the target channel, and verify destination IDs before use. <br>
Risk: Research topics and video metadata may be processed by external services. <br>
Mitigation: Avoid sensitive internal research topics unless Anthropic, Google, Discord, and YouTube handling is acceptable for the intended use. <br>
Risk: Dependency risk is called out for axios in the authoritative security guidance. <br>
Mitigation: Audit or update axios and the package lock before production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dalime/youtube-outlier-skill) <br>
- [Publisher profile](https://clawhub.ai/user/dalime) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Text and Markdown summaries, Google Sheets rows, Discord messages, TypeScript code, shell commands, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured YouTube, Google Sheets, Discord, and Anthropic credentials for full operation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
