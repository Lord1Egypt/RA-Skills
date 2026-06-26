## Description: <br>
Control TRIGGERcmd computers remotely by listing and running commands via the TRIGGERcmd REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rvmey](https://clawhub.ai/user/rvmey) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to inspect available TRIGGERcmd commands and trigger selected commands on computers registered to the authenticated TRIGGERcmd account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can trigger TRIGGERcmd actions on computers tied to the configured token, including commands that change files, services, devices, or system state. <br>
Mitigation: Review available commands before use, require confirmation for side-effecting actions, and start with known-safe commands. <br>
Risk: The TRIGGERcmd API token grants remote command access if exposed. <br>
Mitigation: Prefer a temporary TRIGGERCMD_TOKEN environment variable, keep any token file owner-only with chmod 600, and never print or log token values. <br>


## Reference(s): <br>
- [TRIGGERcmd Website](https://www.triggercmd.com) <br>
- [TRIGGERcmd API](https://www.triggercmd.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash and jq command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and jq with a TRIGGERCMD_TOKEN environment variable or owner-only token file.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
