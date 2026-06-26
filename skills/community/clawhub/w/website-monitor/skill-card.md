## Description: <br>
Lightweight website uptime monitor that checks URL availability, measures response times, detects content changes with hashes, and verifies expected response text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[claudiodrusus](https://clawhub.ai/user/claudiodrusus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, site operators, and automation agents use this skill to check whether one or more websites return expected status codes, expected content, and stable content hashes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes live network requests to user-provided URLs, which may reveal that the running environment accessed a target endpoint. <br>
Mitigation: Confirm each URL before running the skill, especially for internal services or sensitive endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/claudiodrusus/website-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text status summaries or JSON arrays from command-line execution examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns process exit code 1 when any checked site fails the expected status or validation checks.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
