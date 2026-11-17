## Description:

Creates a structured pre-showing brief for real estate visits, covering buyer profile, property focus areas, route and timing notes, on-site questions, risks, and post-showing records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External real estate agents and client-facing property teams use this skill to turn buyer requirements, listing details, and showing schedules into a reviewable Markdown brief before a property visit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input may include buyer, listing, schedule, or other sensitive materials beyond what is needed for the showing brief.

Mitigation: Provide only the buyer, listing, and schedule information needed for the brief, and redact unrelated sensitive information before use.

Risk: A showing brief can become misleading if missing listing or disclosure information is filled in without support.

Mitigation: List missing information as items to confirm, avoid fabricating property facts, and verify important details against formal disclosures.

Risk: Unused generic audit modes in the local script broaden the apparent behavior of an otherwise focused structured-brief skill.

Mitigation: Use the skill for structured real-estate showing briefs, avoid broad project directories as input, and document or remove inactive audit modes in a future release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/real-estate-showing-brief)
- [README](artifact/README.md)
- [Structured brief specification](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)
- [Example output](artifact/examples/example-output.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured Markdown, with optional JSON output when run through the local script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a reviewable draft, highlights missing information, and avoids adding facts beyond the provided local input.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
