## Description: <br>
Use when medium-to-large changes need explicit requirements, technical design, and task planning before implementation, especially for multi-module work, unclear acceptance criteria, or architecture-heavy requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binggg](https://clawhub.ai/user/binggg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to decide when a coding request needs a structured requirements, design, and task-planning workflow before implementation. It helps agents produce concise spec documents with explicit acceptance criteria and staged confirmation for larger or ambiguous changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can slow larger coding tasks by requiring requirements, design, task planning, and confirmation steps. <br>
Mitigation: Use the full workflow only for medium-to-large or ambiguous changes; skip it for small, clear, low-risk edits. <br>
Risk: The skill may create planning files in the workspace. <br>
Mitigation: Review generated requirements, design, and task files before relying on them or starting implementation. <br>
Risk: The skill may reference external CloudBase documentation links. <br>
Mitigation: Review external references before using them as project guidance. <br>


## Reference(s): <br>
- [Spec Workflow raw source](https://cnb.cool/tencent/cloud/cloudbase/cloudbase-skills/-/git/raw/main/skills/cloudbase/references/spec-workflow/SKILL.md) <br>
- [CloudBase main skill entry](https://cnb.cool/tencent/cloud/cloudbase/cloudbase-skills/-/git/raw/main/skills/cloudbase/SKILL.md) <br>
- [UI design companion skill](https://cnb.cool/tencent/cloud/cloudbase/cloudbase-skills/-/git/raw/main/skills/cloudbase/references/ui-design/SKILL.md) <br>
- [Data model companion skill](https://cnb.cool/tencent/cloud/cloudbase/cloudbase-skills/-/git/raw/main/skills/cloudbase/references/data-model-creation/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown planning documents and concise workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create requirements.md, design.md, and tasks.md under a specs directory when the full workflow is used.] <br>

## Skill Version(s): <br>
1.18.7 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
