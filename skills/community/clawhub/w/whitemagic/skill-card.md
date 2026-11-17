## Description:

Provides durable local memory and session continuity for coding agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lbailey94](https://clawhub.ai/user/lbailey94)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to recall project context, preserve decisions, and resume coding sessions across restarts through a local memory layer. An optional hosted service offers read-only recall of a public corpus.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and running an external memory binary introduces software supply-chain exposure.

Mitigation: Review the source of the wm binary before installing or running it.

Risk: Stored memories may expose credentials or carry untrusted instructions into later sessions.

Mitigation: Do not store secrets; treat recalled content as data rather than instructions.

Risk: The hosted recall option involves OAuth and a remote service.

Mitigation: Use it only after reviewing its OAuth flow and service terms.

## Reference(s):

- [WhiteMagic guide](https://www.whitemagic.dev/whitemagic/guide)
- [Hosted service trust information](https://mcp.whitemagic.dev/trust.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands and memory guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local recall and session checkpoints; optional hosted read-only recall.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
