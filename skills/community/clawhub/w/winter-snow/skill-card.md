## Description: <br>
Plan winter snow trips for ski resorts, Harbin ice festival visits, snow village stays, hot springs in snowy regions, aurora viewing, and related travel bookings through Fliggy-powered flyai CLI results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to answer winter travel requests with live flyai CLI results, including destinations, hotels, attractions, transportation, itineraries, and booking links. It is intended for snow, ski, ice festival, hot spring, and aurora travel planning scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to install and use an unpinned global npm CLI before answering travel queries. <br>
Mitigation: Review the flyai CLI package before installation, approve global installs deliberately, and prefer an isolated or project-local installation when possible. <br>
Risk: The skill can route users into a Fliggy-backed booking flow where personal, travel, or payment details may be entered. <br>
Mitigation: Avoid entering sensitive personal or payment details unless the user intentionally proceeds with the provider's booking service. <br>


## Reference(s): <br>
- [Winter Snow Travel ClawHub release](https://clawhub.ai/dingtom336-gif/winter-snow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with conclusion-first travel recommendations, comparison tables, and booking links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output and should include Fliggy booking links for listed results.] <br>

## Skill Version(s): <br>
3.2.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
