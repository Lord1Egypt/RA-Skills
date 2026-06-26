## Description: <br>
Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use for complex artifacts requiring state management, routing, or shadcn/ui components - not for simple single-file HTML/JSX artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pupuking723](https://clawhub.ai/user/pupuking723) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold and bundle complex Claude HTML artifacts with React, TypeScript, Vite, Tailwind CSS, shadcn/ui, and Parcel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included scripts install npm packages, may install pnpm globally, and modify frontend project files. <br>
Mitigation: Run the scripts only in a fresh or intended project directory and review package and configuration changes before committing. <br>
Risk: The initialization script depends on shadcn-components.tar.gz, which security evidence says is missing from the artifact. <br>
Mitigation: Confirm the component archive is present or update the script before relying on the initializer. <br>


## Reference(s): <br>
- [shadcn/ui components](https://ui.shadcn.com/docs/components) <br>
- [ClawHub release page](https://clawhub.ai/pupuking723/web-artifacts-builder-anthropic) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and generated frontend project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a React project scaffold and a bundled single-file HTML artifact when its scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
