## Description: <br>
Provides top 3 surf spots in a region ranked by wave height, wind direction, and wind speed using Surfline data and a defined scoring rubric. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wertopter](https://clawhub.ai/user/wertopter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Surfers and surf-planning agents use this skill to compare supported regions or supplied Surfline spot IDs and choose the best surf spots for a forecast window. The agent runs the bundled data-collection script, scores all valid spots, and returns the top three with concise scoring explanations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a bundled local Python script that makes network requests to Surfline using the selected region or spot IDs. <br>
Mitigation: Install only if this Surfline data sharing and local script execution are acceptable for the intended environment. <br>
Risk: Surf conditions and API responses can change, so ranked recommendations may be stale or incomplete. <br>
Mitigation: Use current forecast windows, review excluded or failed spots, and avoid inventing missing data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wertopter/surf-spot-finder) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with ranked results and scoring explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run a local Python data-collection script that can emit JSON or text from Surfline forecast data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
