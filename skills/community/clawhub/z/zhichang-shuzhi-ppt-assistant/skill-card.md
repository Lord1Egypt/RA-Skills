## Description:

Generates workplace report PPT materials from user-provided knowledge-base content through a staged workflow that clarifies goals, builds a SPEC and outline, then optionally creates a PPTX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bz-ai](https://clawhub.ai/user/bz-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workplace presentation authors use this skill to turn fragmented work records, project documents, meeting notes, data tables, and similar materials into structured workplace reporting presentations for performance reviews, promotion defenses, project updates, proposals, retrospectives, planning, and management decision briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated PPTX speaker notes include an automatic author contact credit on the final slide.

Mitigation: Review generated PPTX files before sharing and remove the contact credit from speaker notes if it is not desired.

Risk: Workplace source material may include secrets, confidential business details, or regulated data.

Mitigation: Provide only the minimum materials needed and redact secrets or regulated data before using the skill.

Risk: The optional PPTX generator depends on local Python packages.

Mitigation: Install dependencies in a pinned virtual environment before running the script.

## Reference(s):

- [Narrative Structures](references/narrative-structures.md)
- [Expression Conversion](references/expression-conversion.md)
- [Chart Suggestions](references/chart-suggestions.md)
- [Quality Checklist](references/quality-checklist.md)
- [PPTX Generation Script](scripts/generate_pptx.py)
- [Example Slides JSON](assets/example-slides.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown planning artifacts, JSON slide definitions, shell commands, PPTX files, speaker notes, and text reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated PPTX workflow can also produce chart placeholder lists, missing-data lists, replaceable-content lists, and risk expression checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
