## Description: <br>
Generates five-layer architecture analysis and DrawIO-based architecture diagrams from source code structure and dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect a repository, map source files and dependencies into a standardized five-layer architecture, and generate diagrams and supporting analysis for review or documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can modify system or global tools and overwrite a Dockerfile in the current directory. <br>
Mitigation: Run installation from a controlled working directory or isolated environment, and review expected file changes before use. <br>
Risk: Git hooks, weekly sync, or commit-triggered automation may operate on under-specified repositories or schedules. <br>
Mitigation: Enable automation only after defining the exact repository, files, schedule, trigger conditions, and removal process. <br>
Risk: Source analysis reads repository contents and dependency structure. <br>
Mitigation: Use the skill only on repositories the user intends to inspect and avoid running it on unrelated or sensitive workspaces. <br>


## Reference(s): <br>
- [Source To Architecture on ClawHub](https://clawhub.ai/vincentlau2046-sudo/source-to-architecture) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON, DrawIO, PNG, SVG, or PDF artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local repository scanning and optional diagram export tooling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
