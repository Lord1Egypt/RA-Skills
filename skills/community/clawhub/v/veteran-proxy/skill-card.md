## Description: <br>
Helps agents guide users through managing the veteran proxy client, including subscription updates, node listing, SOCKS5 proxy start and stop commands, status checks, split-routing rules, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veteran-cli](https://clawhub.ai/user/veteran-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need agent guidance for installing, configuring, operating, or troubleshooting the veteran proxy CLI for subscription-based proxy nodes and local SOCKS5/HTTP routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proxy node operators or subscription providers may observe connection metadata and some traffic depending on encryption. <br>
Mitigation: Verify the veteran CLI package and proxy node provider before use, and avoid sending sensitive credentials through untrusted nodes. <br>
Risk: Proxy use may conflict with workplace, school, or regional policies. <br>
Mitigation: Confirm that proxy use is permitted in the user's environment before configuring or starting the service. <br>


## Reference(s): <br>
- [Veteran Proxy ClawHub page](https://clawhub.ai/veteran-cli/veteran-proxy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proxy subscription, routing-rule, environment-variable, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
