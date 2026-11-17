## Description:

Parses supported documents into Markdown or structured JSON through xparse-cli so agents can read, convert, summarize, or prepare document content for downstream work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaorui921](https://clawhub.ai/user/zhaorui921)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and document-processing agents use this skill to turn local documents or document URLs into readable Markdown or structured JSON before summarization, extraction, review, or other downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing xparse-cli may require downloading and executing vendor-hosted installer code.

Mitigation: Review the installer before execution or use a verified package source before enabling the skill.

Risk: Parsing documents can send sensitive document content to the TextIn/xparse service.

Mitigation: Avoid confidential, regulated, or client documents unless external processing is approved for the use case.

Risk: Document passwords and TextIn credentials can be exposed through command lines, shell history, config files, or CI settings.

Mitigation: Prefer interactive credential setup or protected secrets storage, avoid inline real passwords where possible, and restrict access to saved APP_ID and SECRET_CODE values.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhaorui921/skills/textin-xparse-parser-safe)
- [API Reference](references/api-reference.md)
- [CLI Guidance](references/cli-guidance.md)
- [Error Handling](references/error-handling.md)
- [TextIn Key Setup](references/textin-key-setup.md)
- [TextIn Parse API v1](https://docs.textin.com/xparse/v1/)
- [TextIn Documentation](https://docs.textin.com/)
- [TextIn Console](https://www.textin.com/console/dashboard/setting)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples; parsed document output may be Markdown or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires xparse-cli and may use the external TextIn/xparse service; default guidance favors serial parsing and asks for missing passwords, credentials, or page ranges instead of silently retrying.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
