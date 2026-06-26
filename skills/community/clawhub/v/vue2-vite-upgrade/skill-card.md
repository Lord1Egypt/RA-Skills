## Description: <br>
Helps developers migrate Vue 2 projects from Webpack or Vue CLI build setups to Vite, including configuration, environment variable compatibility, code migration, validation, and optional deployment updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yyyyzj](https://clawhub.ai/user/yyyyzj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and execute Vue 2 project migrations from Webpack to Vite while preserving business dependencies, converting configuration, and checking common runtime issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup steps can delete Webpack-era files from the wrong project or before work is backed up. <br>
Mitigation: Confirm the project root, require a clean Git state or backup, review exact deletion targets, and prefer git rm so changes can be restored. <br>
Risk: Deployment configuration could expose credentials or trigger an unintended production upload. <br>
Mitigation: Use environment variables for deployment credentials and require explicit confirmation before production deployment. <br>
Risk: Dependency migration may preserve vulnerable or incompatible package versions. <br>
Mitigation: Review dependency changes, resolve peer conflicts manually before using force installs, and verify axios against current security guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yyyyzj/vue2-vite-upgrade) <br>
- [Vite configuration reference](references/vite-config.md) <br>
- [Migration steps reference](references/migration-steps.md) <br>
- [Common issues reference](references/common-issues.md) <br>
- [Deployment configuration reference](references/deploy-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
