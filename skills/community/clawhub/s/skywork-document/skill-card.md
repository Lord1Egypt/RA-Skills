## Description:

Skywork Document generates professional documents in DOCX, PDF, HTML, and Markdown through the Skywork Office Doc API, optionally using uploaded reference files and server-side web search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gxcun17](https://clawhub.ai/user/gxcun17)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create structured documents such as reports, proposals, resumes, plans, summaries, and translated or rewritten documents. The skill can generate from a prompt alone or use uploaded reference files as source material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full prompts and selected reference files may be sent to Skywork for remote processing.

Mitigation: Use the skill only with content approved for Skywork processing, and avoid confidential documents unless organizational policy permits it.

Risk: The skill requires a SKYWORK_API_KEY and includes setup guidance that can expose secrets if handled carelessly.

Mitigation: Store the key in a protected secret store or permissioned configuration and avoid printing it in terminal output.

Risk: Generated documents are downloaded locally from a remote service.

Mitigation: Inspect downloaded files before opening them or using them in later workflows.

Risk: Broad auto-use instructions may trigger remote document generation for long structured writing tasks.

Mitigation: Confirm the user's intent and remote-processing acceptability before uploading files or sending detailed prompts.

## Reference(s):

- [Skywork Document on ClawHub](https://clawhub.ai/gxcun17/skills/skywork-document)
- [Skywork API Key Setup Guide](references/apikey-fetch.md)
- [Skywork](https://skywork.ai)
- [Skywork API Key Settings](https://skywork.ai/?openApiKeySetting=1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands and final document links; generated files may be DOCX, PDF, HTML, or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKYWORK_API_KEY; may upload reference files and downloads generated files locally.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
