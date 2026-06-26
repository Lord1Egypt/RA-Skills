## Description: <br>
Create new skills, modify and improve existing skills, and measure skill performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plabzzxx](https://clawhub.ai/user/plabzzxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to draft, evaluate, iterate on, benchmark, and package agent skills. It is intended for skill creation and improvement workflows across agent platforms that can read skill files and run local Python tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can run local Python automation, use subagents or the Claude CLI, and open local review pages. <br>
Mitigation: Review scripts before use, run in a controlled workspace, and prefer static review output when a local server is unnecessary. <br>
Risk: Description optimization may send skill and evaluation content to Anthropic. <br>
Mitigation: Do not use confidential skills, customer data, or secrets with optimization workflows unless the data-sharing path has been approved. <br>
Risk: Evaluation runs and logs may persist sensitive transcripts or generated files. <br>
Mitigation: Keep evaluation workspaces free of secrets and delete or restrict access to generated workspaces after review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/plabzzxx/skill-creator-claude) <br>
- [README](artifact/README.md) <br>
- [Evaluation schemas](artifact/references/schemas.md) <br>
- [Claude Code](https://claude.ai/code) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, generated files, and packaged skill artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create evaluation workspaces, benchmark reports, review pages, and .skill package files when the user asks to run the full workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
