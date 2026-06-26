## Description: <br>
Adjust morning weather briefing location based on travel plans captured from conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suidge](https://clawhub.ai/user/suidge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal-agent operators use this skill to keep a morning weather briefing aligned with saved travel plans. It captures city-level travel dates from conversation, stores them in a local travel-plan file, cleans past entries, and falls back to a default home location when no trip is active. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores home and travel cities plus dates in a local travel-plan file and may update that file from travel-related conversation. <br>
Mitigation: Install only if this local storage is acceptable, and review or delete the travel-plan file when plans are private or captured incorrectly. <br>
Risk: The selected city is sent to wttr.in for the weather lookup. <br>
Mitigation: Avoid using the weather lookup when sharing city-level location with that service is not acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/suidge/travel-morning-weather) <br>
- [Homepage](https://github.com/Suidge/travel-morning-weather) <br>
- [Capture Triggers](references/capture-triggers.md) <br>
- [Data Format](references/data-format.md) <br>
- [Morning Briefing Integration](references/morning-briefing.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses python3 and curl; reads and updates a local travel-plan JSON file for city-level morning weather selection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
