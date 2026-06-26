## Description: <br>
Travel Emergency Assistant helps agents respond to disrupted trips by producing three-option emergency plans for canceled flights, overbooked hotels, closed attractions, and weather-related changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uasnu1111](https://clawhub.ai/user/uasnu1111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-support agents use this skill during urgent trip disruptions to identify the scenario, request live flight, hotel, or attraction options through FlyAI CLI, and return a concise three-choice decision card with prices, booking links, trade-offs, and risk notes. <br>

### Deployment Geography for Use: <br>
Global, subject to FlyAI and booking-link coverage. <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask an agent to install and run a third-party global npm CLI before travel searches can work. <br>
Mitigation: Install and vet @fly-ai/flyai-cli in a contained environment before use, avoid sudo when possible, and only proceed if the operator accepts the persistent CLI dependency. <br>
Risk: Travel prices, availability, and booking links can change quickly or be incorrect if the live search data is stale. <br>
Mitigation: Verify prices, seat or room availability, and booking terms on the linked booking page before purchasing or changing travel plans. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/uasnu1111/travel-emergency-assistant) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown decision card with booking links and optional shell commands for FlyAI CLI setup or execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live travel search results when FlyAI CLI is available; prices and availability should be verified on the booking page.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact metadata reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
