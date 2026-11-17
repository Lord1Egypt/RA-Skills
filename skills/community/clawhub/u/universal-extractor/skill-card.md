## Description:

Extract clean text from URLs, articles, documents, and files. Four extraction micro-services. Use when you need to pull content from web pages, PDFs, or any file format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renoblabs](https://clawhub.ai/user/renoblabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract clean text and article summaries from URLs, PDFs, DOCX/TXT documents, and other uploaded files through paid x402 extraction endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted URLs and encoded document or file contents are sent to the extraction service.

Mitigation: Use the skill only for content you are authorized to submit, and avoid secrets, internal-only documents, personal data, or regulated data unless provider data-handling terms have been reviewed.

Risk: The documented endpoints require x402 USDC payments.

Mitigation: Confirm that the agent operator accepts the listed fees before using the endpoints.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/renoblabs/skills/universal-extractor)

## Skill Output:

**Output Type(s):** [guidance, API calls, text, JSON]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Service responses may include extracted text, titles, authors, summaries, dates, word counts, and USDC x402 payment requirements.]

## Skill Version(s):

1.0.0 (source: server release evidence, created 2026-04-11T06:42:12Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
