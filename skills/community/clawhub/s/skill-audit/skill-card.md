## Description: <br>
Audit locally installed agent skills for security and policy issues using the SkillLens CLI and produce a risk-focused report from each skill's SKILL.md and bundled resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morozRed](https://clawhub.ai/user/morozRed) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to scan local Codex or Claude skill directories with SkillLens, triage unsafe or suspicious results, and prepare evidence-based audit reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow asks users to run or install the external SkillLens CLI. <br>
Mitigation: Verify that the SkillLens package is the intended package before use, and prefer one-off or pinned execution over a global install. <br>
Risk: Scanning broad configured roots may expose more local skill content than intended. <br>
Mitigation: Scan a specific skills directory whenever possible instead of all configured roots. <br>
Risk: Optional auditor CLIs may process local skill content outside the immediate scan command. <br>
Mitigation: Use optional auditor CLIs only for content that is acceptable to share with those tools. <br>


## Reference(s): <br>
- [SkillLens Audit on ClawHub](https://clawhub.ai/morozRed/skill-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Audit reports may include each reviewed skill's name, path, verdict, risk score, evidence, and recommended fixes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
