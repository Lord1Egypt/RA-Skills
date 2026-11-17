## Description:

Professional Ziwei Doushu consultation skill with offline, Beijing-standard calculation rules for birth-date reports that separate chart facts, traditional interpretation, and practical trend summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spyfree](https://clawhub.ai/user/spyfree)

### License/Terms of Use:

MIT-0

## Use Case:

External users and practitioners use this skill to generate structured Ziwei Doushu readings from birth date, time, gender, and optional yearly context. It is suited for transparent traditional chart analysis that distinguishes calculated facts from interpretive guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional chart export can write SVG or JPG files to a default or user-provided path.

Mitigation: Run the skill in a normal non-privileged workspace and choose an explicit chart output path before generating chart files.

Risk: Python, npm, and optional chart-rendering dependencies affect local execution behavior.

Mitigation: Pin and review Python and npm dependencies before use, especially when enabling the optional JS engine or JPG rendering path.

Risk: Traditional Ziwei Doushu interpretation may be mistaken for deterministic or professional advice.

Mitigation: Keep chart facts separate from interpretation and preserve the stated boundary that outputs are not medical, legal, or financial advice.

Risk: The optional JS engine path may fail or differ if local dependencies are missing or versions drift.

Mitigation: Use dual-engine discrepancies as review signals and document any dependency setup needed for the JS engine.

## Reference(s):

- [Time Mapping and Longitude Correction](references/mapping.md)
- [Interpretation Framework](references/interpretation-framework.md)
- [ClawHub Skill Page](https://clawhub.ai/spyfree/skills/ziwei-doushu)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, files, guidance]

**Output Format:** [Markdown or JSON report, with optional SVG or JPG chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline execution; optional chart export may require additional local rendering dependencies.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
