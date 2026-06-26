## Description: <br>
Learning Growth Coach helps users define human skill goals, log practice sessions, diagnose bottlenecks, plan deliberate practice, and track progress in local Markdown notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals, coaches, and productivity-oriented developers use this skill to turn broad learning goals into structured milestones, practice logs, progress reviews, and next-session plans. It is intended for human learning and coaching workflows, not for self-modifying agent code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Practice logs may contain personal goals, performance notes, or other sensitive learning details in local Markdown files. <br>
Mitigation: Keep `.learnings` in a private directory, avoid recording secrets or highly sensitive personal details, and exclude the notes from sync or version control unless intentional. <br>
Risk: The quick-log helper appends local practice entries based on user-provided skill names. <br>
Mitigation: Run the helper only in the intended workspace and review generated `.learnings/skills/*.md` entries before sharing or committing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/self-improving-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown coaching guidance with local Markdown log templates and optional bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or append `.learnings/skills/*.md` practice notes when the quick-log helper is used.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
