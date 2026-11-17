## Description:

structured-extraction helps agents turn authorized unstructured text, webpages, and PDFs into machine-readable JSON using schema-first prompting, JSON mode, few-shot examples, output priming, and a JSON repair helper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to design reliable extraction prompts and clean model outputs before downstream JSON processing. It is intended for public or authorized source material such as documents, webpages, PDFs, and data pipeline inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JSON repair helper may make invalid or incomplete model output appear usable.

Mitigation: Treat repaired output as provisional and validate it with an authoritative schema or downstream parser before use.

Risk: The learner helper writes notes and preferences to persistent files.

Mitigation: Avoid recording sensitive information and use it only where persistent local learning files are acceptable.

Risk: The skill is intended for extraction from public or authorized material only.

Mitigation: Do not use it on personal, confidential, or classified documents unless separate authorization and controls are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/structured-extraction)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce cleaned JSON files when the bundled repair helper is run.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
