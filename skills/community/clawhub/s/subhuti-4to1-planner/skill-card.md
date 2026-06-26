## Description: <br>
AI planning coach using the 4To1 Method to turn a 4-year vision into daily action across Notion, Todoist, Google Calendar, or local Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dorjenorbulim](https://clawhub.ai/user/dorjenorbulim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and teams use this skill to set up and maintain a goal-planning workflow that connects long-term vision, quarterly milestones, two-week sprints, and daily tasks. It supports guided onboarding, weekly and quarterly reviews, progress checks, and task capture through the user's chosen planning backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can require OAuth tokens or API keys for productivity services and may access sensitive planning data. <br>
Mitigation: Use least-privilege credentials, share only the intended Notion page with the integration, keep the local config file private, and choose the local Markdown backend when privacy is the priority. <br>
Risk: Backend writes to Notion, Todoist, Google Calendar, or local files could introduce unwanted planning changes. <br>
Mitigation: Ask the agent to preview important changes before writing them and review generated tasks, milestones, and status updates before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dorjenorbulim/subhuti-4to1-planner) <br>
- [4To1 Planner website](https://4to1planner.com) <br>
- [4To1 Planner free starter kit](https://4to1planner.com/free-download.html) <br>
- [4To1 Planner templates](https://4to1planner.com/shop.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Conversational guidance and Markdown with inline shell commands or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or write planning data through the selected backend when the user grants credentials and confirms the intended workflow.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
