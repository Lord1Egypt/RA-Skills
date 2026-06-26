## Description: <br>
Orchestrator for GitHub Spec-Kit SDD workflow in OpenClaw. Use when starting a new project with spec-driven development, setting up spec-kit toolchain, or running through the full SDD pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[staok](https://clawhub.ai/user/staok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to initialize and run an OpenClaw spec-driven development workflow around GitHub Spec-Kit, including project setup, specification, planning, task generation, implementation batching, and coding guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup installs unpinned external tools and skills from GitHub. <br>
Mitigation: Run `setup.sh --check-only` first, review the external sources reported by setup, and install only in an environment where live third-party downloads are acceptable. <br>
Risk: The workflow can delete `.claude` and `CLAUDE.md` during project initialization. <br>
Mitigation: Run initialization only in a prepared project directory and preserve any needed `.claude` or `CLAUDE.md` content before executing cleanup steps. <br>
Risk: Using `--force` can replace existing external skills. <br>
Mitigation: Avoid `--force` unless replacement is intended and existing skill directories have been reviewed or backed up. <br>


## Reference(s): <br>
- [GitHub Spec-Kit](https://github.com/github/spec-kit) <br>
- [Top-Level Coding Guidance](CodingGuidance/TopLevelCodingGuidance.md) <br>
- [C++ Coding Style](CodingGuidance/CppCodingStyle.md) <br>
- [Design Pattern Guidance](CodingGuidance/DesignPattern/DesignPattern.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, file paths, and generated project documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to create or update project files such as README.md, DEVLOG.md, .specify artifacts, specs, tasks, and implementation changes.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
