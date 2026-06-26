## Description: <br>
Integrates with Tesla's official Fleet API to configure OAuth, read vehicle or energy device data, and issue signed remote vehicle commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to set up Tesla Fleet API credentials, manage OAuth tokens, list vehicles, inspect vehicle status, and run remote vehicle actions such as wake, climate, lock, honk, and charging controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive Tesla account tokens, vehicle data, and location-related information when configured. <br>
Mitigation: Keep the workspace private, protect auth.json and private-key.pem, and avoid sharing generated state files or logs. <br>
Risk: Remote commands can affect a physical vehicle, including climate, charging, locks, horn, lights, and wake actions. <br>
Mitigation: Require explicit user confirmation before running commands that change vehicle state. <br>
Risk: The local signing proxy and private key are needed for signed vehicle commands. <br>
Mitigation: Run the proxy only when needed, stop it when finished, and protect the private key material. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/odrobnik/tesla-fleet-api) <br>
- [Publisher profile](https://clawhub.ai/user/odrobnik) <br>
- [Tesla vehicle-command proxy](https://github.com/teslamotors/vehicle-command) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute or propose local Python and shell scripts that call Tesla Fleet API endpoints when configured.] <br>

## Skill Version(s): <br>
1.5.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
