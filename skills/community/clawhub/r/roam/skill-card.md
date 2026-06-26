## Description: <br>
Interact with Roam HQ via REST API to search meetings, get transcripts, prompt transcripts with AI, send messages, and manage groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robfig](https://clawhub.ai/user/robfig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams with Roam HQ access use this skill to retrieve meeting context, summarize or analyze transcripts, and post follow-up messages to Roam groups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read private meeting transcripts and chat history when given a Roam API token. <br>
Mitigation: Use the least-privileged Roam token available and avoid using it for highly sensitive meetings unless necessary. <br>
Risk: The skill can post messages to Roam groups. <br>
Mitigation: Require the agent to show the target group and exact message text before any Roam message is posted. <br>


## Reference(s): <br>
- [Roam API Documentation](https://developer.ro.am) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or text responses based on Roam API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ROAM_API_KEY; respect Roam API rate limits of 10 burst and 1 request per second sustained.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
