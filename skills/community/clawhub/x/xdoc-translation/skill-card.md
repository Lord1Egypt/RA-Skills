## Description:

Document and text translation API skill powered by Xdoc for translating files and text across many languages with glossary and translation-memory support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangsongbai1](https://clawhub.ai/user/yangsongbai1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to guide Xdoc document and text translation workflows, including file upload, translation submission, status polling, result download, glossary management, and translation-memory operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents and text may be sent to Xdoc's cloud service for translation.

Mitigation: Use the skill only for content approved for Xdoc processing, and avoid confidential files unless the account, policy, and retention expectations are acceptable.

Risk: The required Xdoc API key is tied to an account and quota.

Mitigation: Keep XDOC_API_KEY out of logs and shared files, rotate or revoke exposed keys, and monitor usage against the account quota.

Risk: File deletion, glossary, and translation-memory changes can affect user-managed resources.

Mitigation: Keep delete and library modification operations explicitly user-directed and confirm target IDs before issuing API calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangsongbai1/skills/xdoc-translation)
- [Xdoc translation service](https://translation.x-doc.ai/)
- [Xdoc provider site](https://x-doc.ai)
- [Xdoc privacy policy](https://x-doc.ai/privacy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include endpoint parameters, polling steps, request examples, and user-directed file, glossary, or translation-memory operations.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
