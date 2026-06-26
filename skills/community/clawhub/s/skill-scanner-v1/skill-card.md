## Description: <br>
skill-scanner reviews SKILL.md-format agent skills for malicious patterns, permission abuse, prompt injection, and ClawHavoc attack vectors, then reports a Safe, Caution, or Danger verdict. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billyhetech](https://clawhub.ai/user/billyhetech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to vet OpenClaw, Claude Code, GitHub, local, or pasted SKILL.md content before deciding whether to install or trust a skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Static skill review can miss runtime behavior that is not visible in SKILL.md content. <br>
Mitigation: Treat reports as advisory and review GitHub issues, ClawHub community feedback, and runtime behavior before installation. <br>
Risk: Scanning local paths or pasted content may expose sensitive information to the reviewing agent. <br>
Mitigation: Avoid providing files or skill text that contain secrets, credentials, or private operational details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/billyhetech/skill-scanner-v1) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown safety report with check-level findings, verdict, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses static analysis only; evidence provenance says no server-resolved GitHub import provenance is stored for this version.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
