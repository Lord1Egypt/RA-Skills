## Description: <br>
Query flight information, train tickets, and travel data using the Variflight API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lyz1990](https://clawhub.ai/user/lyz1990) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to look up flight routes, flight status, airport weather, train tickets, flight prices, transfers, and flight comfort metrics through Variflight. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends travel queries to the Variflight API. <br>
Mitigation: Install and use it only when sending those travel queries to Variflight is acceptable for the task and environment. <br>
Risk: The skill requires a Variflight API key, and exposed keys could be leaked through command-line history, committed config files, Docker images, or shared settings. <br>
Mitigation: Use a protected environment variable or secret manager, avoid passing the key on the command line, keep local key files permission-restricted, and do not commit or bake live keys into shared artifacts. <br>


## Reference(s): <br>
- [Variflight AI](https://ai.variflight.com) <br>
- [Variflight API endpoint](https://ai.variflight.com/api/v1/mcp/data) <br>
- [ClawHub skill listing](https://clawhub.ai/lyz1990/variflight) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration guidance, Text] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VARIFLIGHT_API_KEY or an equivalent local configuration file.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
