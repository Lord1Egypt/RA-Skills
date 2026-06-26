## Description: <br>
Travel visa advisor that helps outbound travelers check visa requirements, application locations, and trip-preparation steps for a known destination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-support agents use this skill to check visa requirements, application paths, required materials, timelines, and nearby visa center or consulate options for planned outbound trips. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Visa requirements or processing timelines may be incomplete, outdated, or inconsistent across search results. <br>
Mitigation: Verify visa conclusions with official government, embassy, consulate, or visa center sources before booking or traveling. <br>
Risk: Travel-planning details and optional API credentials may be sent to FlyAI/Fliggy services through the CLI workflow. <br>
Mitigation: Use the skill only when the FlyAI CLI package and service are trusted, configure a dedicated API key if needed, and avoid sharing unnecessary personal details. <br>


## Reference(s): <br>
- [FlyAI homepage](https://open.fly.ai/) <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/travel-visa) <br>
- [Playbooks](references/playbooks.md) <br>
- [Templates](references/templates.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with checklists, tables, links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses booking or jump links from FlyAI/Fliggy outputs when present; visa conclusions should be verified with official sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
