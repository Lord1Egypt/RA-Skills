## Description: <br>
Find water parks - epic water slides, wave pools, lazy rivers, and splash zones - and support related travel services such as flights, hotels, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, and car rental through Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search for water parks and related travel options by collecting city and optional attraction parameters, running the FlyAI CLI, and formatting provider-backed booking results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs the agent to install an unpinned global third-party FlyAI CLI before answering travel queries. <br>
Mitigation: Ask for explicit confirmation before installation, verify the npm package source and version, and prefer a controlled environment for CLI execution. <br>
Risk: Returned booking links and travel results come from the provider-backed CLI rather than an independent survey of all available options. <br>
Mitigation: Present booking links as provider-backed results and encourage users to compare critical travel purchases against other sources before booking. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/water-park) <br>
- [Publisher profile](https://clawhub.ai/user/dingtom336-gif) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on FlyAI CLI results and include provider booking links when results are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
