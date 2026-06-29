## Description: <br>
Stellar Trails provides an always-on six-phase workflow for agent tasks, with planning, traceability, verification gates, and adaptive complexity across coding, document, visualization, data-processing, and question-answering work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hoshiyomix](https://clawhub.ai/user/hoshiyomix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to structure work into repeatable phases, preserve traceability, and require verification before delivery. It is intended for broad task execution workflows, including code changes, documents, visualizations, data processing, planning, and direct answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run broad local setup, update itself, write persistent logs or memory, and start a local preview server. <br>
Mitigation: Review dev.sh and the activation steps before use, and disable auto-update, preview-server, dependency-install, or persistent-memory behavior unless those behaviors are explicitly needed. <br>
Risk: The workflow is highly opinionated and activates for a broad range of tasks. <br>
Mitigation: Install it only when an always-on structured workflow is desired, and review generated plans, commands, and reports before acting on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hoshiyomix/skills/stellar-trails) <br>
- [README](README.md) <br>
- [AskUserQuestion Gate Template](references/askuserquestion-gate.md) <br>
- [SADC Subagent Delegation Template](references/sadc-subagent-delegation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with optional code blocks and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output adapts to task complexity and may include phase plans, traceability IDs, verification notes, reports, and implementation artifacts.] <br>

## Skill Version(s): <br>
7.9.4 (source: evidence.json release, SKILL.md metadata, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
