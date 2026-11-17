## Description:

Incrementally imports Telegram messages from a local SQLite database into a LanceDB vector store using Qwen3-Embedding-4B embeddings served by LM Studio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lulu-owo](https://clawhub.ai/user/lulu-owo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to index exported Telegram message data into a local LanceDB vector store for retrieval and downstream agent workflows. It is most relevant when the user controls the source database, local embedding service, and destination storage path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles private Telegram message content and sends message text to a local LM Studio embeddings endpoint.

Mitigation: Run only in an environment where the user controls the Telegram database and LM Studio service, and confirm that message content is permitted to be indexed.

Risk: The checkpoint uses pickle, which can execute unsafe data if the checkpoint file is tampered with.

Mitigation: Protect the checkpoint path from untrusted writes or replace the checkpoint mechanism with a safer serialization format before routine use.

Risk: Failed embedding batches can be treated as processed without being written to LanceDB.

Mitigation: Review import logs and checkpoint behavior after failures, and rerun from a known-good checkpoint when batch writes fail.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lulu-owo/skills/telegram-import)
- [Publisher Profile](https://clawhub.ai/user/lulu-owo)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with Python script execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for running a local Telegram-to-LanceDB import workflow; the artifact includes a Python script that writes embeddings and checkpoint files.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
