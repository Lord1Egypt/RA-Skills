## Description: <br>
Learning Capture helps an agent record corrections, failed tool runs, recurring gotchas, and feature requests as redacted, project-scoped markdown notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brasco05](https://clawhub.ai/user/brasco05) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-assisted teams use this skill to capture user corrections, failed tool runs, recurring project gotchas, and feature requests as reviewable notes before promoting durable lessons into agent instructions with approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project learning notes may include sensitive details if failures or corrections are copied too broadly. <br>
Mitigation: Keep notes redacted, avoid credentials, tokens, private messages, customer data, and full logs, and review `.learnings/` files before committing or sharing the repository. <br>
Risk: Promoting a note into durable agent instructions could preserve incorrect or overly broad guidance. <br>
Mitigation: Treat durable instruction changes as proposals and require explicit user approval before editing agent rules or configuration. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown notes and a brief text confirmation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or appends project-scoped `.learnings/` notes without overwriting existing notes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
