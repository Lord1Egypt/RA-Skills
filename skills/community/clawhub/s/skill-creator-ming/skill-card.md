## Description: <br>
Create new skills, modify and improve existing skills, and measure skill performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wm-zqbx](https://clawhub.ai/user/wm-zqbx) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and skill authors use this skill to draft, revise, evaluate, benchmark, and package agent skills through an iterative review workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and modify skill files and produce generated descriptions or guidance that may be incorrect or overly broad. <br>
Mitigation: Review generated skill content, descriptions, and benchmark outputs before deployment. <br>
Risk: The bundled workflow can run local Python helpers, call the local Claude CLI, and launch a localhost review viewer. <br>
Mitigation: Use a dedicated workspace, avoid secrets in eval prompts or outputs, prefer static viewer mode when possible, and choose an unused viewer port. <br>
Risk: The security review marked the release suspicious because local automation can stop unrelated services and encourages broad skill triggering. <br>
Mitigation: Inspect local automation behavior before use and keep trigger descriptions specific enough to avoid unrelated activations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wm-zqbx/skill-creator-ming) <br>
- [Publisher Profile](https://clawhub.ai/user/wm-zqbx) <br>
- [Schemas Reference](references/schemas.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks, JSON schemas, generated files, benchmark reports, and review viewer output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify skill files, evaluation workspaces, packaged skill archives, benchmark artifacts, and local/static review viewer files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
