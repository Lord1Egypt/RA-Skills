## Description:

Extract structured data from construction specifications. Parse CSI sections, requirements, submittals, and product data from spec documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Developers, construction project managers, estimators, and procurement teams use this skill to extract CSI sections, submittals, product requirements, referenced standards, and structured summaries from construction specification documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read local files selected for construction specification processing.

Mitigation: Grant filesystem access only for documents intended for analysis and avoid providing unrelated or sensitive files.

Risk: Unpinned document-processing dependencies can change behavior across installations.

Mitigation: Install dependencies in a virtual environment and pin pdfplumber before production use.

Risk: Prompts outside the intended construction specification scope may produce misleading structured summaries.

Mitigation: Keep usage scoped to construction specification extraction and review generated sections, submittals, product data, and standards before relying on them.

## Reference(s):

- [Data Driven Construction homepage](https://datadrivenconstruction.io)
- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/skills/specification-extractor)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown tables and structured summaries, with optional CSV, Excel, or JSON export guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes user-provided construction specification inputs and filesystem paths when supplied by the user.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
