## Description:

Turns a target keyword and a page goal into a writer-ready content brief with the title, meta and heading limits checked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US in-house SEO managers, freelance writers, and agencies use the skill to structure an SEO content brief around search intent, page goals, required entities and links, and sourced claims. The bundled workflow produces a Markdown validation report for a supplied brief; it does not generate a complete brief.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The bundled workflow returns a validation report rather than a complete writer-ready brief, and its heading checks need correction.

Mitigation: Review the report manually, correct heading checks before relying on them, and complete the brief using the reference and template.

Risk: Running the workflow replaces seo-content-brief.md in the chosen output folder.

Mitigation: Choose an output folder where replacing that file is acceptable.

Risk: The optional Windows app is unsigned and outside the security review; its supplied checksum does not establish safety.

Mitigation: The app is unnecessary for this workflow; skip it and use the bundled Python workflow.

## Reference(s):

- [SEO content brief rules](artifact/references/content-brief-rules.md)
- [ClawHub skill page](https://clawhub.ai/rapidworker1/skills/seo-content-brief-builder)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown validation report with field checks and guardrails]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checks selected brief fields and reports missing fields or configured length-limit issues; it is not a complete content brief.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
