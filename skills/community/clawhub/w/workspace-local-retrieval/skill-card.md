## Description: <br>
Builds a local-first retrieval architecture for OpenClaw workspaces with explicit corpus boundaries, deny-by-default agent access, separate personal-memory and workspace-knowledge layers, stable search interfaces, and maintenance-aware refresh workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ys-c-23](https://clawhub.ai/user/ys-c-23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, bootstrap, and review safer local workspace retrieval systems without indexing everything by default. It helps separate workspace knowledge from personal memory, define agent-scoped corpus access, and plan refresh and smoke-test workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated corpus allowlists or exclude globs may be too broad for a workspace before indexing begins. <br>
Mitigation: Review and narrow generated corpus configuration before running any indexing or embedding refresh workflow. <br>
Risk: Using --force can overwrite existing retrieval templates. <br>
Mitigation: Use --force only when overwriting templates is intentional and review the generated files afterward. <br>
Risk: Remote embedding APIs can introduce privacy and cost tradeoffs. <br>
Mitigation: Prefer local embedding backends unless the user explicitly accepts remote processing, cost, and data-handling implications. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ys-c-23/workspace-local-retrieval) <br>
- [Privacy and Boundaries](artifact/references/privacy-and-boundaries.md) <br>
- [Agent Scoping](artifact/references/agent-scoping.md) <br>
- [Interface Contract](artifact/references/interface-contract.md) <br>
- [Dependencies and Platforms](artifact/references/dependencies-and-platforms.md) <br>
- [Preflight and Install Policy](artifact/references/preflight-and-install-policy.md) <br>
- [Runtime Layout](artifact/references/runtime-layout.md) <br>
- [Maintenance Patterns](artifact/references/maintenance-patterns.md) <br>
- [Design Rationale](artifact/references/design-rationale.md) <br>
- [Sanitized Demo](artifact/references/sanitized-demo.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration templates and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write sanitized retrieval/config JSON templates when the CLI bootstrap is run; it does not index or upload data by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
