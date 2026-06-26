## Description: <br>
Guides agents through a skill installation workflow that requires pre-install vetting, rejects configuration-changing installs, and keeps user instructions as the controlling authority. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TerryRen2024](https://clawhub.ai/user/TerryRen2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to guide discovery, vetting, and installation of agent skills while avoiding configuration changes unless the user gives explicit direction. It is best treated as workflow guidance, not as an independent security control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create false confidence because the included installer reports SAFE TO INSTALL from mocked safety checks. <br>
Mitigation: Do not rely on the script verdict; independently vet the exact skill source, review all files and installation steps, and use a real security review before installing. <br>
Risk: The workflow allows arbitrary external sources such as GitHub repositories, local directories, or other user-provided sources. <br>
Mitigation: Use only intended and trusted sources, verify provenance from server evidence when available, and avoid installing from unreviewed locations. <br>
Risk: Search terms, private repository names, or secrets may be exposed through logs or shell commands during installation workflows. <br>
Mitigation: Avoid logging secrets, private repository names, and sensitive queries; keep credentials such as COMPOSIO_API_KEY out of command history and reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TerryRen2024/skill-install-manager-1-0-0) <br>
- [Publisher profile](https://clawhub.ai/user/TerryRen2024) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and procedural instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the clawhub CLI; references COMPOSIO_API_KEY as an optional environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
