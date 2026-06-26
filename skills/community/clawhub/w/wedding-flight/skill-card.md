## Description: <br>
Book wedding and honeymoon flights with flexible date ranges and seat class options, powered by Fliggy through the flyai CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liquanyu123](https://clawhub.ai/user/liquanyu123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-booking agents use this skill to collect wedding or honeymoon flight parameters, run real-time flyai searches, and present bookable flight options with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install and run an unpinned global third-party CLI. <br>
Mitigation: Manually verify or pin the @fly-ai/flyai-cli package version before use, and run it in a contained environment. <br>
Risk: Travel search details are sent to FlyAI/Fliggy through the CLI. <br>
Mitigation: Use the skill only when sharing itinerary details with that provider is acceptable for the user and deployment context. <br>


## Reference(s): <br>
- [Parameter and Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Fallback Procedures](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/liquanyu123/wedding-flight) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results must be derived from flyai CLI output and include booking links when presenting flight options.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
