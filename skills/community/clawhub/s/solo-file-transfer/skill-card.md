## Description:

Solo File Transfer converts Word documents to Markdown with extracted images and uploads files, webpages, or notes to an IMA knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meta-evo-creator](https://clawhub.ai/user/meta-evo-creator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base operators use this skill to convert .docx files into Markdown assets and move documents, webpages, or notes into an IMA knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local documents and notes to remote IMA/Tencent COS services using user credentials.

Mitigation: Review each file, webpage, or note before upload and do not send sensitive content unless the destination knowledge base is appropriate.

Risk: Credential handling is required for IMA API and COS upload operations.

Mitigation: Provide credentials through trusted environment variables or local credential files, avoid command-line secrets, and rotate credentials if exposure is suspected.

Risk: Changing IMA_BASE_URL or the baseUrl option can redirect authenticated requests to a different endpoint.

Mitigation: Use the default endpoint unless the alternate endpoint is explicitly trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meta-evo-creator/skills/solo-file-transfer)
- [IMA service](https://ima.qq.com)
- [Tencent Cloud COS PUT Object documentation](https://cloud.tencent.com/document/product/436/7778)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, generated Markdown files, extracted image files, and API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.7+, python-docx, Node.js, IMA credentials, and user-selected local files or IMA knowledge-base targets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
