## Description:

Public APIs Skill Creator helps agents find free public APIs, compare access requirements, generate curl, Python, and JavaScript usage examples, and scaffold custom API skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[547895019](https://clawhub.ai/user/547895019)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to discover public API options for a requested task, inspect authentication, HTTPS, CORS, and documentation details, and generate starter API call templates or a new API-focused skill scaffold.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated API scripts can embed untrusted URLs into executable code.

Mitigation: Review generated scripts and validate the exact HTTPS host and endpoint before running them.

Risk: Generated scripts may send bearer tokens to unvalidated destinations.

Mitigation: Do not set API_TOKEN for generated scripts until the destination host and endpoint have been confirmed from trusted documentation.

Risk: The --try option may probe catalog links that have not been verified.

Mitigation: Avoid using --try on unverified catalog links and inspect the selected API documentation first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/547895019/skills/public-apis-skill-creator)
- [public-apis catalog README content endpoint](https://api.github.com/repos/public-apis/public-apis/contents/README.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and curl, Python, and JavaScript code examples; generated files when scaffolding a skill.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated examples may require endpoint validation and token handling before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
