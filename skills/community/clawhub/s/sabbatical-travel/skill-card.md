## Description: <br>
Book flights for sabbatical and long-break travel, with related travel-booking guidance powered by Fliggy (Alibaba Group). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivan97](https://clawhub.ai/user/ivan97) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to search sabbatical, career-break, and long-break flight options through the flyai CLI, then present bookable results with real-time pricing links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install and run the unpinned third-party @fly-ai/flyai-cli package globally. <br>
Mitigation: Preinstall or approve a trusted pinned CLI version before use, and review CLI execution before allowing the agent to proceed. <br>
Risk: Travel searches are processed through the external flyai/Fliggy service and may include itinerary details. <br>
Mitigation: Share only the minimum itinerary information needed for the search and avoid unnecessary personal or sensitive travel details. <br>
Risk: The security review recommends limiting use to flight searches. <br>
Mitigation: Use this release for flight-search workflows unless a separate review approves broader hotel, train, attraction, visa, insurance, or car-rental behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivan97/sabbatical-travel) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands, comparison tables, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses flyai CLI output as the travel data source; final responses should include booking links and avoid raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
