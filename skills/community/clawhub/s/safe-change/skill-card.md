## Description: <br>
Map blast radius before shipping by surfacing importers, affected API routes, test gaps, environment variables, and recent migrations when editing shared TypeScript code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brasco05](https://clawhub.ai/user/brasco05) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use Safe Change before modifying shared TypeScript services, controllers, hooks, routes, or utilities to understand impact, test gaps, configuration risk, and whether to proceed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The verification gate runs the target repository's own package scripts. <br>
Mitigation: Review package.json scripts before running the gate and use the narrowest applicable project root. <br>
Risk: The static scanner can miss dynamic imports, barrel re-exports, decorator aliases, path aliases, and non-TypeScript files. <br>
Mitigation: Treat a low score as advisory on complex codebases and manually check the documented blind spots when they apply. <br>
Risk: The skill does not require credentials, purchase authority, or crypto-related access. <br>
Mitigation: Do not grant credentials, spending permission, or crypto access when using this skill. <br>


## Reference(s): <br>
- [Usage Guide](references/usage.md) <br>
- [Limitations](references/limitations.md) <br>
- [Example Impact Report](references/example-impact-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with JSON-derived risk details and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a Low, Medium, or High risk score and a mandatory go/no-go checkpoint before edits.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
