## Description: <br>
Find whitewater rafting, river tubing, and other water adventure experiences, from gentle family floats to extreme rapids, using Fliggy-powered flyai CLI results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to search for rafting, tubing, and water-adventure attractions by city and format real-time flyai CLI results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can ask the agent to install a global flyai CLI dependency automatically. <br>
Mitigation: Review the package and installation command before allowing global installation, and prefer an environment where global npm changes are acceptable. <br>
Risk: Travel requests may be retained in a local .flyai-execution-log.json file. <br>
Mitigation: Avoid entering passport numbers, payment details, confirmation codes, or sensitive personal information, and remove the log file when retained query history is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/rafting-spots) <br>
- [Templates - rafting-spots](references/templates.md) <br>
- [Playbooks - rafting-spots](references/playbooks.md) <br>
- [Fallbacks - Attraction Category](references/fallbacks.md) <br>
- [Runbook - Execution Log Schema](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output as the source of travel results; final results should include booking links and a flyai attribution tag.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
