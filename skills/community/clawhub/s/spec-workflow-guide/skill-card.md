## Description: <br>
Use when medium-to-large changes need explicit requirements, technical design, and task planning before implementation, especially for multi-module work, unclear acceptance criteria, or architecture-heavy requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binggg](https://clawhub.ai/user/binggg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to decide when a medium-to-large coding change needs a structured requirements, design, and task workflow before implementation. It helps agents produce requirements, design, and task documents with user confirmation between phases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add unnecessary planning overhead for small or already precise changes. <br>
Mitigation: Apply its own decision rule and skip the full workflow for small, low-risk tasks with clear scope and acceptance criteria. <br>
Risk: Requirements, design, or task plans may be incomplete or misaligned with user intent. <br>
Mitigation: Review each generated spec phase and require user confirmation before moving from requirements to design, from design to tasks, and from tasks to implementation. <br>
Risk: The skill may create project spec files as part of normal use. <br>
Mitigation: Review generated files under the specs directory before implementation and keep task status tied to confirmed requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/binggg/skills/spec-workflow-guide) <br>
- [CloudBase main entry](https://cnb.cool/tencent/cloud/cloudbase/cloudbase-skills/-/git/raw/main/skills/cloudbase/SKILL.md) <br>
- [Current skill raw source](https://cnb.cool/tencent/cloud/cloudbase/cloudbase-skills/-/git/raw/main/skills/cloudbase/references/spec-workflow/SKILL.md) <br>
- [UI design companion skill](https://cnb.cool/tencent/cloud/cloudbase/cloudbase-skills/-/git/raw/main/skills/cloudbase/references/ui-design/SKILL.md) <br>
- [Data model companion skill](https://cnb.cool/tencent/cloud/cloudbase/cloudbase-skills/-/git/raw/main/skills/cloudbase/references/data-model-creation/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown spec documents and concise planning guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create requirements.md, design.md, and tasks.md under a specs directory when the full workflow is appropriate.] <br>

## Skill Version(s): <br>
1.18.6 (source: server release metadata; artifact frontmatter reports 2.23.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
