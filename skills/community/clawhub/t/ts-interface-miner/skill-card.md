## Description:

Ts Interface Miner analyzes TypeScript .ts and .tsx files to locate API/interface definitions from feature keywords, function names, or API paths and generate structured Markdown table documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[9talk](https://clawhub.ai/user/9talk)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to inspect TypeScript API code, extract request and response details, and produce readable Markdown documentation for interface review or handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated API documentation may include inferred HTTP methods or status codes.

Mitigation: Review generated Markdown against the source TypeScript before using it as authoritative API documentation.

Risk: Analyzing private code exposes that code to the current agent session.

Mitigation: Use the skill only on code the user is authorized and comfortable to analyze in the active agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/9talk/skills/ts-interface-miner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code]

**Output Format:** [Markdown tables with TypeScript code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include inferred HTTP methods or status codes and explicit notes for missing comments or unresolved external type references.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
