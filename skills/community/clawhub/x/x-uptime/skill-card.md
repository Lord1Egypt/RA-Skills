## Description: <br>
Enhanced `uptime` with structured YAML output showing uptime, users, and 1/5/15-minute load averages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwinjhlee](https://clawhub.ai/user/edwinjhlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system operators use this skill through x-cmd to check local system uptime, logged-in user count, and 1/5/15-minute load averages in YAML or raw uptime output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a separate x-cmd installation that is not bundled in the artifact. <br>
Mitigation: Install x-cmd only from a trusted source and verify it before running x uptime commands. <br>
Risk: The command reports local system status such as uptime, load averages, and logged-in user count. <br>
Mitigation: Use it only in environments where exposing basic operational status is acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/edwinjhlee/x-uptime) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and YAML-style output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a separate trusted x-cmd installation and reports local uptime, user count, and load averages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
