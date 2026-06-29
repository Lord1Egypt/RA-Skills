## Description: <br>
Audits installed agent-skill packages using usage, overlap, burden, risk, and optional ablation or community evidence to recommend cleanup actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gongyu0918-debug](https://clawhub.ai/user/gongyu0918-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent administrators use this skill to inventory installed agent skills, evaluate usage and overlap, review risk signals, and produce conservative cleanup recommendations before removing or merging skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Usage and history inputs can contain sensitive conversation content, local paths, project names, or customer data. <br>
Mitigation: Provide the narrowest skills root and avoid passing history files unless the user is comfortable with the tool reading those exports. <br>
Risk: Cleanup recommendations could cause loss of useful skills if treated as automatic actions. <br>
Mitigation: Review report recommendations manually before deleting, merging, or quarantining any skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gongyu0918-debug/skills/skill-usefulness-audit) <br>
- [Project homepage](https://github.com/gongyu0918-debug/skill-usefulness-audit) <br>
- [Ablation Protocol](references/ablation-protocol.md) <br>
- [Scoring Rubric](references/scoring-rubric.md) <br>
- [Report Narration Prompt](references/report-narration-prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown report with optional JSON audit data and ablation plan files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations are manual-review guidance; the skill does not automatically delete, merge, or quarantine installed skills.] <br>

## Skill Version(s): <br>
0.3.7 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
