## Description: <br>
Find international SIM cards and eSIM plans for overseas travel, including data packages, local numbers, and destination coverage, with related travel booking support powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-focused agents use this skill to search for international SIM card and eSIM options for a destination, compare available plans, and return booking links from flyai CLI results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to install and use an unpinned global flyai npm CLI. <br>
Mitigation: Install the CLI yourself from a trusted source, review the installed package and version before use, and avoid automatic global installation in restricted environments. <br>
Risk: The skill can persist raw travel queries and execution details in `.flyai-execution-log.json`. <br>
Mitigation: Review, rotate, or disable the local log before use, and avoid entering sensitive passport, visa, payment, or detailed itinerary data unless the CLI and log handling are acceptable. <br>
Risk: Booking recommendations and prices depend on external flyai CLI results and provider links. <br>
Mitigation: Confirm price, coverage, validity period, and booking terms on the linked provider page before purchase. <br>


## Reference(s): <br>
- [Travel Simcard Skill Page](https://clawhub.ai/dingtom336-gif/travel-simcard) <br>
- [Publisher Profile](https://clawhub.ai/user/dingtom336-gif) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown comparison tables with booking links and inline shell commands when setup or retries are needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs must be based on flyai CLI results, include booking links from detailUrl, and match the user's input language.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
