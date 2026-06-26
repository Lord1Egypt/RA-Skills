## Description: <br>
Book flights for wine tours to vineyards and wine regions, with related travel booking support for hotels, trains, attractions, itineraries, visas, insurance, and car rental through Fliggy/flyai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liquanyu123](https://clawhub.ai/user/liquanyu123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel agents use this skill to find wine-tour flight options and related travel services from flyai CLI output, then present bookable Markdown results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to install an unpinned global npm package before running searches. <br>
Mitigation: Require manual approval for installation, review the @fly-ai/flyai-cli package/source, and prefer a pinned version in a controlled environment. <br>
Risk: The skill sends travel search details to the flyai/Fliggy CLI provider and relies on provider-returned booking links. <br>
Mitigation: Avoid sensitive travel details unless the provider is trusted, and review booking links before acting on them. <br>
Risk: The skill runs shell commands to search flights and recover from errors. <br>
Mitigation: Review generated commands before execution and run them with least privilege. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liquanyu123/wine-tour) <br>
- [Parameter Collection & Output Templates](artifact/references/templates.md) <br>
- [Scenario Playbooks](artifact/references/playbooks.md) <br>
- [Failure Recovery](artifact/references/fallbacks.md) <br>
- [Execution Runbook](artifact/references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown flight and travel search results with inline booking links and shell commands for flyai CLI execution or setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results must be based on flyai CLI output and include Book links when returned by the provider.] <br>

## Skill Version(s): <br>
3.2.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
