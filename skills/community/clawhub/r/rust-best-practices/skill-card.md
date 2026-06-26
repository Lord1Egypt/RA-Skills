## Description: <br>
Development guidance for writing idiomatic, performant, and safe Rust code across ownership, error handling, performance, linting, dispatch, API design, and documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill while building Rust code to choose idiomatic ownership, error handling, API design, performance, documentation, linting, and ecosystem patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested cargo commands may install developer tools or run checks across all targets and features in large or sensitive repositories. <br>
Mitigation: Review commands before running them, scope invocations to the intended workspace or crate when appropriate, and avoid executing tool-install or all-target commands without project approval. <br>
Risk: Rust guidance may be misapplied to a codebase with different performance, API stability, or documentation constraints. <br>
Mitigation: Validate changes with the project's tests, Clippy policy, documentation build, and benchmark or profiling evidence before claiming correctness or performance outcomes. <br>


## Reference(s): <br>
- [API Design](references/api-design.md) <br>
- [Clippy Configuration](references/clippy-config.md) <br>
- [Coding Idioms](references/coding-idioms.md) <br>
- [Documentation](references/documentation.md) <br>
- [Ecosystem Patterns](references/ecosystem-patterns.md) <br>
- [Generics and Dispatch](references/generics-dispatch.md) <br>
- [Performance](references/performance.md) <br>
- [Pointer Types](references/pointer-types.md) <br>
- [Type State Pattern](references/type-state-pattern.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with inline Rust, TOML, YAML, and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; suggested cargo commands should be reviewed before execution in large or sensitive repositories.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
