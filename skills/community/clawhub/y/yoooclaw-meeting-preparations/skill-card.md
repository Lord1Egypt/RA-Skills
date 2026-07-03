## Description: <br>
Creates a concise pre-meeting briefing by summarizing recent phone notifications and, when useful, recent web search results around the meeting topic and relevant people. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users use this skill before meetings to quickly gather relevant recent context, organize it by topic, and identify points worth raising during the meeting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may search recent phone notifications, which can expose sensitive meeting, personal, or organizational context. <br>
Mitigation: Confirm the people, topics, applications, and dates that are in scope before use, and avoid using unrelated notification content in the briefing. <br>
Risk: The skill can install or use the byted-web-search dependency for recent external context. <br>
Mitigation: Approve the dependency source and environment change before installation, or run the skill in notification-only mode when web search is not trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vivalavida-say-hi/yoooclaw-meeting-preparations) <br>
- [byted-web-search dependency source](https://skills.volces.com/skills/bytedance/agentkit-samples) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown briefing in conversation text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May degrade to notification-only briefing when web search is unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
