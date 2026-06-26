## Description: <br>
Use when a project needs one or more verifier skills for web, CLI, or API runtime checks that the Verify agent can discover automatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect a project and generate reusable verifier skill folders for web, CLI, or API runtime checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read project structure and write verifier skill folders into the repository. <br>
Mitigation: Run it in the intended repository and review generated files before committing or using them in a verification workflow. <br>
Risk: Generated verifier guidance may include authentication, cleanup, or self-update instructions. <br>
Mitigation: Review those instructions before supplying secrets, enabling cleanup steps, or adopting self-update behavior. <br>


## Reference(s): <br>
- [Verifier Skill Generator on ClawHub](https://clawhub.ai/wimi321/verifier-skill-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with generated skill files and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create one or more project-specific verifier skill folders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
