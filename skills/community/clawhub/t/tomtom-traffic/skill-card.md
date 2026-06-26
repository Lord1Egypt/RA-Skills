## Description: <br>
Provides real-time traffic monitoring, route calculation, and departure planning using the TomTom Traffic API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jkimnw-code](https://clawhub.ai/user/jkimnw-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to check commute traffic, calculate traffic-aware routes, and plan departure times for meetings using a configured TomTom API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route lookups send configured origin and destination coordinates to TomTom. <br>
Mitigation: Review or edit the default home, work, and coffee coordinates before running commands, and use only locations appropriate for sharing with TomTom. <br>
Risk: API-key or quota misuse could affect account security or availability. <br>
Mitigation: Store a dedicated TomTom API key in TOMTOM_API_KEY, apply quota limits, and monitor usage in the TomTom dashboard. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jkimnw-code/tomtom-traffic) <br>
- [TomTom Developer Portal](https://developer.tomtom.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with shell and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Traffic checks require TOMTOM_API_KEY and may send configured route coordinates to TomTom APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
