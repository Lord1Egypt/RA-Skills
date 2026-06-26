## Description: <br>
Guides agents through a six-stage workflow for modeling client and hybrid state, including ownership, server-cache boundaries, async consistency, persistence, DevTools, and testing in modern frontend applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawkk](https://clawhub.ai/user/clawkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose and structure frontend state management patterns for React, Vue, and Svelte applications. It helps diagnose stale UI, duplicate sources of truth, prop drilling, persistence mistakes, and server/client cache boundary issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: State-management recommendations may be applied directly to production architecture without enough review of app-specific ownership, persistence, or cache invalidation constraints. <br>
Mitigation: Review recommendations against the application's framework, data-fetching layer, security requirements, and production change process before implementation. <br>
Risk: Client-side persistence choices can expose sensitive data if applied without security review. <br>
Mitigation: Do not persist sensitive data in browser storage unless the project has explicitly reviewed the XSS and data-retention risks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawkk/state-management) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with checklists and implementation recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance-only skill; no code, install hooks, credential use, or privileged behavior reported by security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
