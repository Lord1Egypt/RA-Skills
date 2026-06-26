## Description: <br>
Calculates traffic-aware route durations, distances, and Google Maps navigation links between user-supplied locations using the Google Routes API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vemec](https://clawhub.ai/user/vemec) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, employees, or agents use this skill to answer route, distance, traffic, and drive-time questions with current Google Routes API data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Origin and destination addresses are sent to Google Routes API and printed in command output. <br>
Mitigation: Treat route addresses as sensitive data and use the skill only when the user accepts sending those locations to Google and displaying them in JSON output. <br>
Risk: The Google Cloud API key can incur quota or billing charges if broadly scoped or overused. <br>
Mitigation: Use a restricted Google Cloud API key limited to Routes API and monitor quota and billing. <br>
Risk: Non-driving modes may still return a Google Maps link with driving travel mode. <br>
Mitigation: Review the JSON mode and route link before presenting non-driving route links as final navigation guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vemec/smart-route) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON object from a Node.js command, with Markdown setup guidance in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and GOOGLE_ROUTES_API_KEY; sends origin and destination addresses to Google Routes API and includes them in stdout.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
