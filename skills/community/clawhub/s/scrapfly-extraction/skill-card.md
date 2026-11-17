## Description:

Extract structured data from web content using the Scrapfly Extraction API with the Python SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scrapfly](https://clawhub.ai/user/scrapfly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to extract structured data from HTML, markdown, text, or scraped web content with Scrapfly prompts, pre-trained extraction models, and custom templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document content passed as `body` or scraped and extracted through this skill is sent to Scrapfly.

Mitigation: Redact secrets, personal data, regulated data, and confidential documents unless that use is approved.

Risk: The skill depends on the external `scrapfly-sdk` package.

Mitigation: Install in a virtual environment and pin `scrapfly-sdk` to a reviewed version.

## Reference(s):

- [Scrapfly Extraction API endpoint](https://api.scrapfly.io/extraction)
- [Saved Extraction Templates](https://scrapfly.io/docs/extraction-api/templates)
- [Extraction rules and templates](https://scrapfly.io/docs/extraction-api/rules-and-template#rules)
- [ClawHub skill page](https://clawhub.ai/scrapfly/skills/scrapfly-extraction)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation with Python and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes API-key setup and privacy cautions for content sent to Scrapfly.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
