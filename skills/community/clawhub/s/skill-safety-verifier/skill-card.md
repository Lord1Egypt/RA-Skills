## Description: <br>
Security-first skill vetting for AI agents before installation, with checks for red flags, permission scope, suspicious patterns, and safety recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ttttstc](https://clawhub.ai/user/ttttstc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to review external skills before installation and receive risk scoring, warnings, and install guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The advisory lookup disables HTTPS verification, which can make the skill's security results unreliable. <br>
Mitigation: Review this skill before installing, use only explicit skill paths or repositories you choose, prefer a pinned reviewed version, and treat its output as one input rather than a final security decision until TLS verification is fixed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ttttstc/skill-safety-verifier) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or terminal text with optional JSON scan results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes risk scores, warnings, and a recommendation based on scanned skill files and dependency advisory checks when available.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
