## Description: <br>
Vibe Coding Blueprint guides agents through a document-driven coding workflow that plans first, works in small verifiable steps, keeps project documentation synchronized, and leaves architecture decisions and root-cause diagnosis with the human developer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoxiangxie](https://clawhub.ai/user/xiaoxiangxie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to structure AI-assisted coding work around architecture planning, small task iteration, synchronized documentation, and deliberate human review during debugging or refactoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate for ordinary coding requests and steer the agent into a documentation-heavy process. <br>
Mitigation: Invoke it explicitly only when a structured plan-first workflow and project documentation updates are desired. <br>
Risk: The workflow encourages creating or updating architecture docs, folder docs, and file headers, which could add maintenance overhead or stale documentation if reviewed casually. <br>
Mitigation: Review proposed documentation changes with the same scrutiny as code changes and keep edits scoped to files affected by the task. <br>


## Reference(s): <br>
- [Vibe Coding Blueprint on ClawHub](https://clawhub.ai/xiaoxiangxie/vibe-coding-blueprint) <br>
- [Publisher profile](https://clawhub.ai/user/xiaoxiangxie) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with prompts, documentation templates, code header examples, and verification steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or update project documentation such as architecture docs, folder docs, file headers, and implementation plans.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
