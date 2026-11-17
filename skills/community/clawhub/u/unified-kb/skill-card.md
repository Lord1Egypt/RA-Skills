## Description:

Captures #kb-tagged content, including links, YouTube videos, text, and files, into Tencent IMA, a local workspace knowledge base, and memory records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sundmop](https://clawhub.ai/user/sundmop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to archive #kb-tagged source material into a unified personal knowledge workflow. It supports web articles, WeChat articles, YouTube transcripts, plain text, and local files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User content, local file contents, and fetched web content may be sent to Tencent IMA and stored in the local workspace or memory records.

Mitigation: Use only with content approved for Tencent IMA and local storage; do not pass secrets, private keys, browser profiles, or internal documents.

Risk: The skill accepts local file paths and URLs, which can expose unintended files or unsafe network destinations.

Mitigation: Restrict use to trusted paths and URLs, and run it where private, loopback, and metadata-network destinations are blocked.

Risk: YouTube subtitle handling depends on a fixed cookie file path.

Mitigation: Protect or relocate the YouTube cookie file before use, and avoid storing browser cookies in shared temporary locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sundmop/skills/unified-kb)
- [Publisher profile](https://clawhub.ai/user/sundmop)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text files plus terminal status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores approved content in Tencent IMA, workspace/kb, memory records, and a rebuilt KB index when configured.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
