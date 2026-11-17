## Description:

Thought-Retriever extracts reusable knowledge crystals from conversation answers and stores them in an ontology-backed memory system for later retrieval and evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[as1113435](https://clawhub.ai/user/as1113435)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill as a post-turn memory hook or command-line tool to extract long-term insights from answers, filter or merge them by confidence and similarity, and write Thought entities for later retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation content and stored memory snippets may be sent to the configured external LLM service.

Mitigation: Require explicit opt-in and user-provided service configuration, and redact sensitive content before extraction or similarity checks.

Risk: Conversation-derived thoughts are saved locally and can influence later behavior without enough user control.

Mitigation: Add retention, deletion, and review or quarantine controls before new memories are reused.

Risk: The artifact behavior includes a bundled API key for the external LLM service.

Mitigation: Remove bundled credentials and load user-provided secrets from a secure configuration path or environment variable.

## Reference(s):

- [arXiv:2604.12231](https://arxiv.org/abs/2604.12231)
- [ClawHub skill page](https://clawhub.ai/as1113435/skills/thought-retriever)

## Skill Output:

**Output Type(s):** [text, JSON, files, shell commands, configuration]

**Output Format:** [JSON status output plus ontology JSONL Thought records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes Thought entities with content, confidence, source, query, and last-accessed metadata; extraction and deduplication use configurable confidence and similarity thresholds.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
