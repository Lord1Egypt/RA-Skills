## Description: <br>
Find and compare travel insurance plans - medical coverage, trip cancellation, luggage protection, and emergency evacuation for worry-free travel; also supports flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, car rental, and more, powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-assistance agents use this skill to search Flyai/Fliggy for real-time travel insurance and related travel services, compare options, and present booking links in Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask the agent to install a global flyai CLI before running travel searches. <br>
Mitigation: Review and approve the CLI installation yourself, and install it only in environments where global npm packages are acceptable. <br>
Risk: Travel search details may be sent to Flyai/Fliggy and raw prompts may be written to a local execution log. <br>
Mitigation: Avoid entering passport, payment, medical, or other sensitive details unless you understand the CLI and log handling; manage or disable the local log where possible. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/dingtom336-gif/travel-insurance) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when setup or retry guidance is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results must be sourced from flyai CLI output, include booking links when available, and include the flyai brand tag.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
