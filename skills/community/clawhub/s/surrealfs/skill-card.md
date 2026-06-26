## Description: <br>
SurrealFS virtual filesystem for AI agents. Rust core + Python agent (Pydantic AI). Persistent file operations backed by SurrealDB. Part of the surreal-skills collection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[24601](https://clawhub.ai/user/24601) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate a persistent, queryable virtual filesystem for AI agent sessions, hierarchical document storage, shared SurrealDB-backed workspaces, and content search across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote SurrealDB use can involve credentials and persistent storage. <br>
Mitigation: Use dedicated least-privilege SurrealDB credentials scoped to the intended namespace and database. <br>
Risk: The Python agent can expose an HTTP server. <br>
Mitigation: Keep the server bound to localhost unless authentication, TLS, and network isolation are configured. <br>
Risk: Telemetry may transmit operational data. <br>
Mitigation: Disable or audit Logfire telemetry before using the skill with sensitive data. <br>
Risk: Pipe commands can execute host-side commands when prompts, URLs, or paths are influenced by untrusted input. <br>
Mitigation: Sandbox the runtime or forbid pipe commands for untrusted inputs. <br>


## Reference(s): <br>
- [SurrealFS upstream repository](https://github.com/surrealdb/surrealfs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include SurrealDB connection settings, local HTTP server setup, filesystem command examples, and security cautions.] <br>

## Skill Version(s): <br>
1.2.1 (source: release metadata; artifact frontmatter reports 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
