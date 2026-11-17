## Description:

Provides Tencent Cloud COS object storage and CI data-processing operations for file storage, image, document, media, content moderation, speech, MetaInsight retrieval, and knowledge-base workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Tencent Cloud COS buckets and objects, run CI processing jobs, create searchable knowledge bases, and receive JSON command results through the bundled Node.js script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Tencent Cloud credentials with COS and CI authority.

Mitigation: Use bucket-scoped sub-account or short-lived STS credentials with the smallest required permissions; do not use root account keys.

Risk: Persistent credential storage can leave secrets on disk, and the security evidence warns not to rely on .env.enc as strong secret storage.

Mitigation: Prefer ephemeral environment variables, avoid --persist unless needed, and delete local .env or .env.enc files when finished.

Risk: The setup flow installs cos-nodejs-sdk-v5 from npm, which adds dependency supply-chain exposure.

Mitigation: Install dependencies before exporting credentials and review or pin dependency versions in controlled environments.

## Reference(s):

- [API Reference](artifact/references/api_reference.md)
- [Tencent Cloud COS Node.js SDK documentation](https://cloud.tencent.com/document/product/436/8629)
- [Tencent Cloud CI documentation](https://cloud.tencent.com/document/product/460)
- [cos-nodejs-sdk-v5 GitHub repository](https://github.com/tencentyun/cos-nodejs-sdk-v5)
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/testtesttesttest)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands call Tencent Cloud APIs and normally return JSON; setup may install a local npm dependency and optionally write credential files.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
