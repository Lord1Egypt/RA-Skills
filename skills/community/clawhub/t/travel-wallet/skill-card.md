## Description: <br>
Search for budget-friendly flights with travel wallet planning, including booking, itinerary, and related travel support powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liquanyu123](https://clawhub.ai/user/liquanyu123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search budget-focused flights, collect route parameters, run flyai CLI searches, and present bookable flight results with wallet-oriented price guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can ask an agent to install and run an unpinned global npm CLI. <br>
Mitigation: Approve CLI installation manually, review the package before use, and run it in an environment appropriate for external network calls. <br>
Risk: The skill is tagged as requiring wallet or sensitive-credential capabilities and may be used near payment or booking workflows. <br>
Mitigation: Avoid giving wallet, payment, account, or credential data to the agent; verify booking links and prices directly before purchase. <br>
Risk: Broad travel triggers could cause real-time flight-search commands to run when the user only intended general travel advice. <br>
Mitigation: Confirm origin, destination, date, and intent before running searches or installing tooling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liquanyu123/travel-wallet) <br>
- [Publisher profile](https://clawhub.ai/user/liquanyu123) <br>
- [Parameter Collection & Output Templates](artifact/references/templates.md) <br>
- [Scenario Playbooks](artifact/references/playbooks.md) <br>
- [Failure Recovery](artifact/references/fallbacks.md) <br>
- [Execution Runbook](artifact/references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown flight-search summaries with booking links and inline CLI commands when setup or execution is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on flyai CLI results and include booking links for returned flight options.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
