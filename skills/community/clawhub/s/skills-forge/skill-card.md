## Description: <br>
Detect repeated capability gaps, convert recurring user needs into candidate skills, scaffold new OpenClaw-compatible skills, and validate them before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sheepxux](https://clawhub.ai/user/sheepxux) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Skill Forge to turn repeated failures, feature requests, and manual workflows into reviewed OpenClaw skill candidates. It supports plan-first generation, validation, hidden smoke evaluation, feedback-driven updates, replay checks, and approval-gated installation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate or update skills and write install plans or local candidate files. <br>
Mitigation: Start with plan modes, review generated candidates before approval, and choose output directories that do not contain unrelated work. <br>
Risk: Optional Telegram approval uses sensitive credentials such as bot tokens or approval secrets. <br>
Mitigation: Protect Telegram bot tokens and approval secrets, provide them through environment configuration, and avoid committing or printing real secrets. <br>
Risk: Scheduled review can inspect OpenClaw learning and feedback files. <br>
Mitigation: Install only when this local review behavior is desired, keep scheduled runs summary-only, and review proposed updates before applying them. <br>


## Reference(s): <br>
- [Skill Forge on ClawHub](https://clawhub.ai/sheepxux/skills-forge) <br>
- [Forge Console](references/forge-console.md) <br>
- [Heuristics](references/heuristics.md) <br>
- [Milestone Architecture](references/milestone-architecture.md) <br>
- [Skill Quality Rubric](references/skill-quality-rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON or text command output, with generated skill files and install plans when scripts are run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write candidate skill directories, validation reports, replay summaries, feedback records, approval requests, install plans, and scheduled review reports depending on the selected command.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence and SKILL.md current version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
