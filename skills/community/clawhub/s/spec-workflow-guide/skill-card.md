## Description: <br>
Use when medium-to-large changes need explicit requirements, technical design, and task planning before implementation, especially for multi-module work, unclear acceptance criteria, or architecture-heavy requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binggg](https://clawhub.ai/user/binggg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to slow medium-to-large implementation work into explicit requirements, design, and task documents before coding. It is most useful when scope, acceptance criteria, architecture, UI behavior, or cross-module changes need staged confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill references external CloudBase fallback URLs that were outside the single inspected artifact. <br>
Mitigation: Review those external fallback URLs before relying on sibling skills in an agent workflow. <br>
Risk: Planning guidance can delay or redirect implementation if applied to small, already well-scoped changes. <br>
Mitigation: Use the skill's skip rule for small, low-risk, precise requests and reserve the full workflow for medium or larger changes. <br>


## Reference(s): <br>
- [Spec Workflow Guide on ClawHub](https://clawhub.ai/binggg/skills/spec-workflow-guide) <br>
- [CloudBase main entry](https://cnb.cool/tencent/cloud/cloudbase/cloudbase-skills/-/git/raw/main/skills/cloudbase/SKILL.md) <br>
- [Current skill raw source](https://cnb.cool/tencent/cloud/cloudbase/cloudbase-skills/-/git/raw/main/skills/cloudbase/references/spec-workflow/SKILL.md) <br>
- [CloudBase UI design fallback](https://cnb.cool/tencent/cloud/cloudbase/cloudbase-skills/-/git/raw/main/skills/cloudbase/references/ui-design/SKILL.md) <br>
- [CloudBase data-model fallback](https://cnb.cool/tencent/cloud/cloudbase/cloudbase-skills/-/git/raw/main/skills/cloudbase/references/data-model-creation/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance for requirements, design, and task planning documents] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces requirements.md, design.md, and tasks.md plans when the workflow is used.] <br>

## Skill Version(s): <br>
1.18.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
