## Description: <br>
Plan educational travel experiences including museum visits, university tours, cultural workshops, historical field trips, and hands-on learning activities, with travel booking support powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to plan study tours and educational trips by collecting travel parameters, running flyai CLI searches, and formatting flight, hotel, and attraction options into booking-ready Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on installing and running the third-party flyai CLI for live travel search results. <br>
Mitigation: Approve the npm installation yourself, prefer npx or an isolated environment when practical, and review CLI behavior before use. <br>
Risk: Travel booking links may lead to external services that request payment or personal travel details. <br>
Mitigation: Review booking links and provider details before entering payment, identity, or itinerary information. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dingtom336-gif/study-tour-test-1775879640) <br>
- [Publisher profile](https://clawhub.ai/user/dingtom336-gif) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should summarize CLI-derived travel options, include booking links where available, and avoid raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
