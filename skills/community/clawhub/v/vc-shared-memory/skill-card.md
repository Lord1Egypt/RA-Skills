## Description: <br>
Shared Memory provides a local shared memory pool for cross-team and cross-session collaboration, including company announcements, project collaboration, knowledge management, employee status tracking, and cross-team links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidme6](https://clawhub.ai/user/davidme6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Shared Memory to maintain a local shared-memory store for announcements, project updates, knowledge entries, employee status, and cross-team handoffs across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plaintext shared-memory records under ~/.shared-memory can expose sensitive team, project, employee, or customer information to local callers. <br>
Mitigation: Do not store secrets, regulated data, private employee information, or sensitive customer/project details; use the skill only for information acceptable to share with local users of the environment. <br>
Risk: Write, delete, restore, and overwrite behavior can change or remove shared-memory records without clear access controls or safety prompts. <br>
Mitigation: Keep an external backup, review operations before running restore/delete/write actions, and treat visibleTo or similar fields as labels rather than privacy controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidme6/vc-shared-memory) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/davidme6) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown context summaries, CLI text output, and local JSON data records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and reads plaintext local data under ~/.shared-memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
