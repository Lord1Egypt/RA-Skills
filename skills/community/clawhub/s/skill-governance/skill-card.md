## Description: <br>
OpenClaw Cognitive Operating & Skill Governance Kernel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxime-Xian](https://clawhub.ai/user/maxime-Xian) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to guide an agent through skill governance, cognitive budget checks, context mounting, task closure, and archival practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can broadly influence when work proceeds, which bundles are mounted, and what task records are stored. <br>
Mitigation: Install only when this governance posture is intended, and override the rules so the agent asks before writing memory files, discarding data, or changing the installed skill set. <br>
Risk: The skill asks agents to prepare summaries for external sync during financial, strategic, or major decision tasks. <br>
Mitigation: Require explicit user approval before any external sync and redact confidential or sensitive material from generated summaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maxime-Xian/skill-governance) <br>
- [Manifest homepage](https://clawhub.com/skills/skill-governance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance and structured task records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request calibration scores and require archived task notes before closure.] <br>

## Skill Version(s): <br>
2.1.0 (source: manifest.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
