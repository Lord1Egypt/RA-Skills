## Description: <br>
Skywork Document generates professional documents in docx, pdf, markdown, and html from a prompt and optional reference files by using the Skywork Office Doc API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gxcun17](https://clawhub.ai/user/gxcun17) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create structured documents such as reports, proposals, resumes, summaries, plans, letters, and articles. It can generate a new document from a prompt or use uploaded files as references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send broad user requests and selected local files to Skywork. <br>
Mitigation: Avoid confidential, regulated, or client-sensitive material unless Skywork's data handling terms have been reviewed. <br>
Risk: The skill requires a Skywork API key for remote document generation. <br>
Mitigation: Store the API key in a secret manager or masked environment configuration rather than displaying it in a terminal. <br>
Risk: Uploaded files may be sent with too little scoping or warning at upload time. <br>
Mitigation: Review the files selected for parsing before running the upload step and include only material needed for the document task. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gxcun17/skywork-document) <br>
- [Skywork API key setup guide](references/apikey-fetch.md) <br>
- [Skywork](https://skywork.ai) <br>
- [Skywork API key settings](https://skywork.ai/?openApiKeySetting=1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown response with document download link, local file path, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated documents may be docx, pdf, html, or markdown; reference files are uploaded to Skywork when provided.] <br>

## Skill Version(s): <br>
1.0.9 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
