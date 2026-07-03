## Description: <br>
Zero-exposure script execution using MGC Blackbox: store scripts encrypted, execute them locally, and return results to the agent without exposing plaintext script content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zkeviny](https://clawhub.ai/user/zkeviny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide agents through storing, sealing, and locally executing encrypted scripts with MGC Blackbox. It is intended for workflows where an agent should receive execution results without directly viewing script plaintext. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored scripts can execute locally with the user's privileges while the agent does not see the plaintext script body. <br>
Mitigation: Require manual approval and provenance review for each stored script before execution, and run scripts with least-privilege local accounts. <br>
Risk: Scripts may access local MGC credentials through the token-backed API. <br>
Mitigation: Avoid broad credentials, scope stored secrets narrowly, and restrict access to the local token file and MGC service. <br>
Risk: The documentation emphasizes hidden encrypted execution without enough consent and scope guidance. <br>
Mitigation: Add operator consent checks and clear execution boundaries to any workflow that uses this skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zkeviny/skills/secure-script-runner) <br>
- [MGC Blackbox project reference](https://github.com/zkeviny/MGC-Blackbox) <br>
- [MGC Blackbox issue tracker](https://github.com/zkeviny/MGC-Blackbox/issues) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown documentation with Python, JSON, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill artifact; no executable files are included.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
