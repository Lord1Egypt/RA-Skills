## Description: <br>
Generates complete React Next.js projects from requirements and UI designs using Ant Design, Tailwind CSS, and Zustand for state management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[batype](https://clawhub.ai/user/batype) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to turn requirement documents and optional UI design images into a scaffolded React and Next.js application. It creates project structure, pages, components, state management stores, styling configuration, and local run instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates files and runs local npm project-generation tooling. <br>
Mitigation: Run it only in a fresh, isolated output directory and inspect generated files before installing dependencies or starting the app. <br>
Risk: Server security evidence reports weak path scoping and input validation for generated file paths. <br>
Mitigation: Avoid requirements that contain parent-directory segments, absolute-path-like names, or untrusted route and component names. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/batype/react-nextjs-generator) <br>
- [Artifact README](artifact/README.md) <br>
- [OpenClaw skill description](artifact/OpenClaw-Skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Generated Next.js project files with text status output and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local project files and expects npm tooling to install dependencies and run the generated app.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
