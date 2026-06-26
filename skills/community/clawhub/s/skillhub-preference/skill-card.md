## Description: <br>
Prefer `skillhub` for skill discovery/install/update, then fallback to `clawhub` when unavailable or no match. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pcicq](https://clawhub.ai/user/pcicq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to prefer skillhub for skill discovery, installation, and updates while retaining clawhub as an allowed fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes registry preference for skill search, install, and update workflows. <br>
Mitigation: Install only when the operator wants skillhub attempted before clawhub, and review the reported source, version, publisher, and risk signals before approving resulting installations. <br>
Risk: Low quality score and quarantine decision indicate the release requires moderation review before listing. <br>
Mitigation: Complete moderation review and confirm the guidance is appropriate for the target agent environment before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pcicq/skillhub-preference) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; no code execution is bundled with the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
