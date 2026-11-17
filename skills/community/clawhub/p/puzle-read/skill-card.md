## Description:

Puzle Read lets an agent save web articles, pre-fetched HTML, local documents, and other supported files to a user's Puzle reading library, then list, retrieve, wait for processing, and semantically search those readings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zinklu](https://clawhub.ai/user/zinklu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to connect a Puzle account, save URLs, uploaded files, or article content into a personal reading library, and search or analyze previously saved readings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send uploaded files, pasted text, private pages, internal documents, or authenticated content to the external Puzle service for processing and storage.

Mitigation: Require explicit user approval for the exact source and destination before uploading, and avoid confidential, internal, regulated, or auth-protected content unless the user has confirmed the service's privacy and retention policies.

Risk: The security verdict is suspicious because private or authenticated content may be routed into Puzle too broadly.

Mitigation: Review before installing and use the skill only when the user intentionally wants content sent to and stored by Puzle.

## Reference(s):

- [Puzle Read homepage](https://read-web.puzle.com.cn)
- [Puzle device authorization](https://read-web.puzle.com.cn/device-auth)
- [ClawHub skill page](https://clawhub.ai/zinklu/skills/puzle-read)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; CLI data commands return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Puzle reading links, reading metadata, retrieved content, search results, summaries, and setup guidance.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
