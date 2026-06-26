## Description: <br>
Multi-agent orchestration for complex TypeScript/Next.js/Convex projects. Phased builds, functional verification, the full playbook for delegating to sub-agents without chaos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelmonetized](https://clawhub.ai/user/michaelmonetized) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to plan and coordinate substantial TypeScript, Next.js, and Convex application builds across phases, contracts, implementation, and verification. It is intended to reduce coordination failures when delegating work to multiple agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated plans or sub-agent work can introduce incorrect, incomplete, or misleading application behavior if accepted without review. <br>
Mitigation: Review generated code and sub-agent work before deployment, and require functional verification of data flow, UI behavior, user flows, and error states. <br>
Risk: The included analytics and replay examples may be too permissive for production privacy requirements. <br>
Mitigation: Tighten PostHog and Sentry replay with consent, masking, sensitive-route exclusions, retention limits, and privacy notices before production use. <br>
Risk: Long-running agent workflows can consume excessive time or resources when applied without project-specific boundaries. <br>
Mitigation: Use the workflow in a dedicated project and set appropriate operational limits for long-running agents. <br>


## Reference(s): <br>
- [Web Architecture on ClawHub](https://clawhub.ai/michaelmonetized/web-architecture) <br>
- [Technical Requirements](artifact/TECH-REQ.md) <br>
- [Coding Standards](artifact/CODING-STANDARDS.md) <br>
- [API Contracts Template](artifact/CONTRACTS-TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with checklists, code snippets, command examples, and project templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only workflow guidance for agent-assisted web application architecture.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
