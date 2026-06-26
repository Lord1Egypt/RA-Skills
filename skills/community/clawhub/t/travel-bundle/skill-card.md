## Description: <br>
Find package deals combining hotel and flights, with support for flight booking, hotel reservations, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and related travel services powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search bundled hotel-and-flight offers and compare them with separately sourced flights and hotels. The skill guides the agent to collect trip parameters, execute the flyai CLI, and format real-time travel results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause an agent to install and run an unpinned global npm package before answering ordinary travel queries. <br>
Mitigation: Review and trust @fly-ai/flyai-cli before installing; prefer installing a known version explicitly and approve CLI execution only in an appropriate environment. <br>
Risk: Travel searches may involve sensitive personal, itinerary, or payment-adjacent details handled by external travel providers. <br>
Mitigation: Avoid entering sensitive personal or payment details until the provider's booking and privacy terms have been reviewed. <br>


## Reference(s): <br>
- [Travel Bundle on ClawHub](https://clawhub.ai/dingtom336-gif/travel-bundle) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output as the source for travel results; raw JSON should be transformed into user-readable Markdown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
