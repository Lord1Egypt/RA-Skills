## Description:

Provides an agent-facing interface for users with a purchased API key to retrieve K12 questions and papers from a third-party question-bank API, search questions, fetch answer explanations, and export structured question sets to Word documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[e953962json](https://clawhub.ai/user/e953962json)

### License/Terms of Use:

MIT-0

## Use Case:

External users and education-content developers use this skill to query a third-party K12 question bank by knowledge point, chapter, paper, or keyword, then present retrieved questions and answer explanations or export structured paper data as a docx file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be exposed when passed on the command line or sent to an untrusted custom API base URL.

Mitigation: Keep QB_API_BASE on the official HTTPS endpoint unless a trusted gateway is required, prefer QB_API_KEY in the environment over --key, and avoid sharing commands or logs that include credentials.

Risk: Word export can overwrite an existing local file at the chosen output path.

Mitigation: Choose export paths deliberately and check whether the destination file already exists before writing.

## Reference(s):

- [Question Bank API reference](references/api_docs.md)
- [Question Bank API provider portal](https://api.xuekubao.com)
- [ClawHub skill page](https://clawhub.ai/e953962json/skills/question-bank-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON API responses, text summaries, and optional docx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided API key; Word export writes a docx file to the selected output path.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
