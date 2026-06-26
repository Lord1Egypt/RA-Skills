## Description: <br>
Helps developers generate Webpack and Vite build configuration guidance, including project setup, plugins, loaders, optimization, code splitting, and migration support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to produce build-tool configuration, loader snippets, and command guidance for Webpack/Vite projects and automation pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence flags a review helper that may default to a nested Codex review with broader authority than a review workflow normally needs. <br>
Mitigation: Install only if the publisher is trusted; before running autoreview, disable the default full-access mode with --no-yolo or AUTOREVIEW_YOLO=0. <br>
Risk: Generated build configuration can change project build behavior, including output cleanup, source map generation, dev-server settings, and dependency expectations. <br>
Mitigation: Review generated configuration before committing it or running builds, and test it in a non-production workspace first. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and generated shell/code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit webpack.config.js templates, loader configuration snippets, and terminal command guidance.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
