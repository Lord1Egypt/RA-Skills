## Description: <br>
Agent skill recommender. Input a user need, task description, or existing skill list; output best matching skills, install rationale, duplicate/merge candidates, and gaps for new skill briefs. Runtime-neutral and not tied to one agent platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to match user needs against an existing skill collection, rank candidate skills, and identify duplicate or merge candidates before installing or building new skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper scripts read SKILL.md files from the skills directory supplied by the user, so recommendations depend on the quality and trustworthiness of that local collection. <br>
Mitigation: Use the skill only on skill collections intended for analysis, and review recommendations before installing, merging, or creating skills. <br>


## Reference(s): <br>
- [Recommendation Rules](references/recommendation-rules.md) <br>
- [Output Schema](references/output-schema.md) <br>
- [Dedup / Avoid-Rebuild Mode](references/dedup-mode.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown recommendations and optional JSON from bundled helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ranked recommendations include match rationale, boundaries, secondary matches, overlap groups, and notes.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
