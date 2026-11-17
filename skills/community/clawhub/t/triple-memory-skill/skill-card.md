## Description:

Triple Memory combines LanceDB auto-recall, Git-Notes structured memory, and file-based workspace search to provide persistent context across sessions and manage decisions, preferences, and tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ktpriyatham](https://clawhub.ai/user/ktpriyatham)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to configure persistent memory across conversation recall, structured Git-Notes records, and workspace file search. It supports preserving session context, decisions, preferences, and task state across sessions and branches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Silent, broad memory capture and recall can preserve sensitive conversation or workspace context without enough user control or disclosure.

Mitigation: Disable or gate autoCapture, autoRecall, and memoryFlush in sensitive workspaces, and make memory writes visible before deployment.

Risk: Recalled memories can introduce stale, sensitive, or untrusted context into future agent responses.

Mitigation: Treat recalled memories as untrusted context and review or prune stored memories before using them in sensitive tasks.

Risk: Embedding-backed memory may send text to an external service depending on plugin configuration.

Mitigation: Confirm the embedding provider and data handling path before enabling memory-lancedb for confidential work.

Risk: The file-search helper writes results to a fixed temporary path.

Mitigation: Replace the fixed /tmp helper file with a per-run secure temporary file before production use.

Risk: The skill depends on memory-lancedb and git-notes-memory behavior outside this package.

Mitigation: Pin and review those dependencies before enabling cross-session memory.

## Reference(s):

- [Triple Memory Setup Reference](references/SETUP.md)
- [Auto Flush Configuration](references/auto-flush-config.json)
- [Triple Memory ClawHub Skill Page](https://clawhub.ai/ktpriyatham/skills/triple-memory-skill)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional memory configuration, command examples, and a workspace search helper script.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
