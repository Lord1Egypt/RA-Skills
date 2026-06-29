## Description: <br>
Generates Chinese-language World Cup soccer match reviews, including concise summaries, match-flow analysis, standout-player notes, and fan-discussion highlights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to produce shareable World Cup soccer match reviews from a specified match, team, player, coach, or post-match event. It can also summarize relevant fan-group or notification discussion when the user requests post-match hot topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may search broad local messaging or notification context for World Cup discussion when apps, groups, channels, or time ranges are not specified. <br>
Mitigation: Specify exact apps, groups, channels, and time ranges; avoid notification-based hot-topic or full-output modes when unrelated private messages may be visible. <br>
Risk: A match that is live or not yet started could be mistaken for a completed match, leading to misleading final-score language or premature conclusions. <br>
Mitigation: Confirm match status and official final-score evidence before producing a post-match review; treat uncertain cases as live or pre-match and label observations as provisional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/yoooclaw-world-cup-post-match-review-scene) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Chinese Markdown match review or live/pre-match summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final output is limited to the requested review content and may incorporate scoped match information and local notification context when requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
