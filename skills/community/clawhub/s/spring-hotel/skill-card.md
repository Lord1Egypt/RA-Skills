## Description: <br>
Finds hot spring hotels, private hot spring rooms, ryokan stays, and related travel booking options using FlyAI and Fliggy-backed real-time search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to search current hot spring hotel options, compare prices and amenities, and produce booking-ready Markdown with links. It is most useful when the user needs fresh hotel availability rather than general destination advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to install and run the third-party @fly-ai/flyai-cli package globally. <br>
Mitigation: Review the package before installation, install it only in an environment where third-party travel-search tooling is acceptable, and avoid running it with elevated privileges. <br>
Risk: Travel searches may expose destinations, dates, budgets, and other trip details to FlyAI or related booking services. <br>
Mitigation: Share only travel details needed for the search and avoid entering sensitive personal information unless the user accepts that disclosure. <br>
Risk: The artifact can persist raw execution details in .flyai-execution-log.json when file writes are available. <br>
Mitigation: Disable or delete the local execution log when it is not needed, especially on shared machines or after searches containing personal trip details. <br>


## Reference(s): <br>
- [Parameter and Output Templates](references/templates.md) <br>
- [Hot Spring Hotel Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/spring-hotel) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown comparison tables with booking links and inline shell commands when setup or retry steps are needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on flyai CLI results and include booking links when hotel results are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
