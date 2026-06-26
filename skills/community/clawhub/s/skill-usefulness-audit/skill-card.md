## Description: <br>
Audit or inventory installed agent-skill packages for cleanup using usage, overlap, burden, risk, and optional ablation/community evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gongyu0918-debug](https://clawhub.ai/user/gongyu0918-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent-workspace maintainers use this skill to audit installed agent skills for retention, overlap, usage, quality burden, static risk hints, and optional ablation or community evidence before making manual cleanup decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads installed skill folders and user-provided usage or history files, which may contain sensitive local paths, project names, or conversation content. <br>
Mitigation: Provide only the folders and evidence files needed for the audit, and avoid sensitive transcript exports unless they are necessary. <br>
Risk: The skill can label skills with delete, merge-delete, or quarantine-review recommendations. <br>
Mitigation: Treat those labels as manual review advice; do not remove, merge, or isolate skills automatically based on the report. <br>
Risk: Generated reports may contain derived details from local skill inventories and provided evidence files. <br>
Mitigation: Review report contents before sharing them outside the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gongyu0918-debug/skills/skill-usefulness-audit) <br>
- [ClawHub metadata homepage](https://github.com/gongyu0918-debug/skill-usefulness-audit) <br>
- [Ablation Protocol](references/ablation-protocol.md) <br>
- [Report Narration Prompt](references/report-narration-prompt.md) <br>
- [Scoring Rubric](references/scoring-rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, optional JSON reports, optional JSON ablation plans, and command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include decision summaries, score tables, recommended actions, missing evidence, quality burden, and risk review when relevant.] <br>

## Skill Version(s): <br>
0.3.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
