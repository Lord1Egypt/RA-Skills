## Description: <br>
Skill Combo coordinates multiple installed skills so an agent can parse combination syntax, assign responsibilities, orchestrate execution, and integrate results for complex tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rfdiosuao](https://clawhub.ai/user/rfdiosuao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to combine two or more installed skills for complex tasks that need coordinated analysis, reminders, communication support, search, or other skill outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Coordinating multiple installed skills can amplify the permissions or side effects of downstream skills. <br>
Mitigation: Use only trusted downstream skills, avoid combining skills that can post publicly, delete data, spend money, access private accounts, or create persistent tasks unless each action is explicitly confirmed, and review any separate runtime implementation before relying on it. <br>
Risk: Broad routing through installed skills may produce unsafe or unintended execution paths without clear safety controls. <br>
Mitigation: Review the proposed skill division of labor before execution and require explicit confirmation for any sensitive or irreversible downstream action. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/rfdiosuao/skill-combo) <br>
- [Publisher profile](https://clawhub.ai/user/rfdiosuao) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown coordination plans, skill assignments, and integrated result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May sequence, parallelize, or conditionally route work across installed skills; practical risk depends on the downstream skills selected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
