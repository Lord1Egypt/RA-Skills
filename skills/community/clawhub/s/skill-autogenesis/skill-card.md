## Description: <br>
Skill Autogenesis helps agents review completed work, identify reusable recurring procedures, and decide whether to create or patch a skill, store a memory note, or take no persistence action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeblackhole1024](https://clawhub.ai/user/codeblackhole1024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add guarded procedural-memory behavior to Hermes, OpenClaw, or similar tool-using agents. It helps classify completed work and choose the lightest persistence action before creating or patching reusable skill files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause an agent to actively maintain procedural memory and create or patch skills when the runtime permits it. <br>
Mitigation: Keep skill-management permissions scoped, require human approval when autonomous persistence is not desired, and review generated or patched skills before deployment. <br>
Risk: Generated or patched skills could accidentally preserve secrets, temporary details, or overfit instructions from a single task. <br>
Mitigation: Review and scan outputs before relying on them, and enforce the skill's guidance to exclude secrets, temporary identifiers, and mostly user-specific data. <br>
Risk: A preference, policy, or one-off result could be misclassified as a reusable procedural skill. <br>
Mitigation: Use the required classification record and hard stop rules so only verified executable procedures with triggers, ordered actions, and verification become skill updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codeblackhole1024/skill-autogenesis) <br>
- [Skill source links](references/sources.md) <br>
- [Classification examples](references/classification-examples.md) <br>
- [Hard stop rules](references/hard-stop-rules.md) <br>
- [Hermes Agent skill creation format](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/creating-skills.md) <br>
- [Hermes Agent skill lifecycle guidance](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md) <br>
- [Hermes Agent skill management tool](https://github.com/NousResearch/hermes-agent/blob/main/tools/skill_manager_tool.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown instructions, classification records, and generated or patched skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce SKILL.md, README.md, reference files, templates, or memory and prompt recommendations when the runtime supports those persistence targets.] <br>

## Skill Version(s): <br>
1.3.2 (source: ClawHub release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
