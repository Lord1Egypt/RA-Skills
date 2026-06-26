## Description: <br>
Skill Optimizer 0330 helps agents analyze, audit, and refactor SKILL.md files with design-pattern guidance while preserving the original skill intent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxiaofeng0811-lgtm](https://clawhub.ai/user/dxiaofeng0811-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to review and improve SKILL.md definitions, especially when auditing quality, refactoring structure, or applying agent-skill design patterns without changing the original purpose. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad high-priority auto-trigger rules may cause the skill to run during unrelated agent conversations. <br>
Mitigation: Narrow triggers to explicit requests to optimize or audit a named SKILL.md file, remove generic standalone triggers such as skill and agent, and require confirmation before any rewrite. <br>
Risk: README installation examples fetch a live GitHub URL that is not backed by server-resolved provenance for this release. <br>
Mitigation: Prefer a pinned, reviewed ClawHub artifact for installation instead of live remote install commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dxiaofeng0811-lgtm/skill-optimizer-0330) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with SKILL.md code blocks, rationale, and validation checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces proposed skill changes for review rather than applying them automatically.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
