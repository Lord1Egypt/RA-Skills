## Description: <br>
SurrealDB Surrealism WASM extension development. Write Rust functions, compile to WASM, deploy as database modules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[24601](https://clawhub.ai/user/24601) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create Rust-based SurrealDB functions, compile them to WebAssembly, and register them as database modules callable from SurrealQL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The quick-start command uses default root credentials for a local SurrealDB example. <br>
Mitigation: Run the commands only against a local or disposable instance, and replace default root credentials with a strong least-privilege account outside isolated testing. <br>
Risk: WASM database modules can execute custom Rust logic inside the database environment. <br>
Mitigation: Review any Rust/WASM module before registering it in a database. <br>
Risk: Surrealism is described as actively in development and not yet stable. <br>
Mitigation: Check compatibility with the target SurrealDB 3.x release before relying on the API in a production workflow. <br>


## Reference(s): <br>
- [SurrealDB Extensions Docs](https://surrealdb.com/docs/surrealdb/extensions) <br>
- [SurrealDB CLI module command](https://surrealdb.com/docs/surrealdb/cli/module) <br>
- [ClawHub skill page](https://clawhub.ai/24601/surrealism) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash, TOML, Rust, and SurrealQL snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for SurrealDB WASM extension development.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
