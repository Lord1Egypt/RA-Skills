## Description:

Use when the user requests a non-trivial tool or repository change where supported capabilities, configuration, or extension points may already fit. Do not use for an obvious routine supported fix.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theangrypit](https://clawhub.ai/user/theangrypit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check whether a product's supported capabilities, configuration, or extension points can meet a requested change before proposing custom work. It also helps keep implementation authority and external ownership boundaries clear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A recommendation may rely on an unsupported capability or misstate which team owns the affected behavior.

Mitigation: Check the relevant version's documentation and source when available, distinguish documented or source-proven behavior from unknowns, and confirm the owner boundary before proposing changes to another team's contract.

## Reference(s):

- [Scenario checks](references/scenario-checks.md)
- [Reference and authorship note](references/provenance.md)
- [Hermes Agent public project reference](https://github.com/NousResearch/hermes-agent)
- [OpenClaw public project reference](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Code, Configuration, Shell commands]

**Output Format:** [Markdown guidance and, when an authorized change is made, code, configuration, or shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tailored to the requested outcome, product version, available evidence, and authorized owner boundary]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
