## Description: <br>
X/Twitter engagement assistant for onboarding, persona learning, Browser Relay browser control, local memory, manual reminders, For You follow suggestions, and Following interaction suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasoncodespace](https://clawhub.ai/user/jasoncodespace) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to review X/Twitter timelines, generate candidate follows, likes, and comments, and execute account actions only after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a logged-in X/Twitter browser session to like, follow, or comment. <br>
Mitigation: Keep per-action approval enabled and require explicit confirmation before every account write. <br>
Risk: The skill stores long-lived local memory about user facts, personas, daily activity, and comment history. <br>
Mitigation: Regularly inspect or delete local memory, especially user facts, personas, and daily logs. <br>
Risk: Browser Relay drives a local browser and should be trusted before use. <br>
Mitigation: Review the Browser Relay package and run it only in an environment where the user accepts browser-control risk. <br>


## Reference(s): <br>
- [X Engagement on ClawHub](https://clawhub.ai/jasoncodespace/x-engagement) <br>
- [Browser Relay](https://github.com/jasonCodeSpace/browser-relay) <br>
- [Browser Operations](artifact/docs/browser-operations.md) <br>
- [Human Behavior and Confirmation](artifact/docs/human-behavior.md) <br>
- [Comment Rules](artifact/docs/comment-rules.md) <br>
- [Memory System](artifact/docs/memory-system.md) <br>
- [Manual Reminders and Maintenance](artifact/docs/cron-jobs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text with inline shell commands, JSON configuration examples, and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include candidate comments, follow or like recommendations, local memory guidance, and Browser Relay commands that require user confirmation before account writes.] <br>

## Skill Version(s): <br>
4.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
