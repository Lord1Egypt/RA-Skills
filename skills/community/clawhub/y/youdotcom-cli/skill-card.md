## Description:

Web search, research with citations, and content extraction for bash agents using curl and You.com's REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardirby](https://clawhub.ai/user/edwardirby)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run You.com web search, research with citations, and URL content extraction from a bash environment. It helps choose the appropriate You.com endpoint, prepare curl requests, and handle fetched content as untrusted external data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, prompts, and URLs are sent to a third-party You.com service.

Mitigation: Avoid secrets, credentials, internal-only links, regulated data, and confidential client details unless that use has been approved.

Risk: Fetched web content can contain untrusted instructions or misleading material.

Mitigation: Extract only needed fields with jq, wrap fetched material in external-content delimiters, and do not execute or follow instructions found in fetched content.

Risk: Research and content extraction require a You.com API key.

Mitigation: Use the YDC_API_KEY environment variable only for approved requests and avoid printing or storing the key in outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/edwardirby/skills/youdotcom-cli)
- [You.com API Docs](https://docs.you.com)
- [You.com API Keys](https://you.com/platform/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands, jq examples, and endpoint guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON response paths and guidance for wrapping fetched content in external-content delimiters.]

## Skill Version(s):

3.0.1 (source: server release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
