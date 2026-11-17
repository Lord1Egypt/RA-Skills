## Description:

Qibook Company Wiki Deepresearch uses Qibook enterprise data to classify Chinese companies and organizations and generate concise Markdown business insight reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinadaas-department](https://clawhub.ai/user/chinadaas-department)

### License/Terms of Use:

MIT-0

## Use Case:

External business, legal, finance, and due diligence users use this skill to research a named Chinese company or organization and produce a structured enterprise wiki report covering governance, business, risk, credit, and growth signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends QIBOOK_ACCESS_KEY to the endpoint configured in QIBOOK_BASE_URL, and the security evidence notes there is no host validation.

Mitigation: Set QIBOOK_BASE_URL only to the official HTTPS endpoint provided by Qibook and rotate QIBOOK_ACCESS_KEY if the endpoint configuration may have been exposed or changed.

Risk: Queried entity names and returned business-risk data may be sent to and printed from the remote workflow.

Mitigation: Use the skill only for intended Qibook enterprise or organization reports and handle generated reports and raw results according to the data sensitivity of the queried entity.

Risk: The artifact includes template language that instructs reports not to reveal AI authorship.

Mitigation: Remove or override AI-concealment language when report transparency or disclosure is required.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/chinadaas-department/skills/qibook-company-wiki-deepresearch)
- [Qibook API credential portal](https://skill.qibook.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with setup guidance and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report length is capped by input data volume; the skill requires python3 plus QIBOOK_ACCESS_KEY and QIBOOK_BASE_URL.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
