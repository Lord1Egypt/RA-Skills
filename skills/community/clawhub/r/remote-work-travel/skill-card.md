## Description: <br>
Helps agents search and format booking options for remote-work travel and workation trips using the flyai CLI, with support for flights and related travel services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivan97](https://clawhub.ai/user/ivan97) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect route details, run supported flyai travel-search commands, and present real-time booking options with booking links. It is intended for remote-work travel and workation planning workflows where current provider data is required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to install an unpinned global npm CLI. <br>
Mitigation: Require manual approval for npm installation and prefer a pinned or sandboxed install before running the skill. <br>
Risk: Flight searches may send route and date details to the provider through the CLI. <br>
Mitigation: Confirm user consent before executing searches and avoid sending unnecessary personal or trip data. <br>
Risk: Booking links can lead to purchase actions. <br>
Mitigation: Review booking links, prices, and itinerary details with the user before any purchase action. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ivan97/remote-work-travel) <br>
- [Parameter collection and output templates](artifact/references/templates.md) <br>
- [Scenario playbooks](artifact/references/playbooks.md) <br>
- [Failure recovery](artifact/references/fallbacks.md) <br>
- [Execution runbook](artifact/references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands when setup is required] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires booking results to include provider detail links and avoids raw JSON in user-facing responses.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
