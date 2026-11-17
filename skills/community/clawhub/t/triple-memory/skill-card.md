## Description:

Complete memory system combining LanceDB auto-recall, Git-Notes structured memory, and file-based workspace search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ktpriyatham](https://clawhub.ai/user/ktpriyatham)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to set up persistent memory across sessions, combining conversation recall, structured decision tracking, and workspace file search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory with automatic capture may store sensitive or unwanted user information across sessions.

Mitigation: Require explicit consent before storing memories, disclose when memory is read or written, and review or delete stored records regularly.

Risk: Silent memory operations can make retention behavior hard for users to notice or control.

Mitigation: Disable silent operation and provide visible controls for memory capture, recall, and deletion.

Risk: A shared temporary file path in the workspace search helper can expose stale or conflicting search output between runs.

Mitigation: Replace the shared /tmp file-search path with a unique mktemp-based file and clean it up after each search.

Risk: Automatically recalled memories may carry stale, irrelevant, or prompt-injected context into future agent work.

Mitigation: Treat recalled memory as untrusted context, allow users to inspect it, and prune outdated or untrusted records.

## Reference(s):

- [Triple Memory Setup Reference](references/SETUP.md)
- [ClawHub Skill Page](https://clawhub.ai/ktpriyatham/skills/triple-memory)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON configuration examples and bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup steps for persistent memory, auto-recall, auto-capture, structured notes, and workspace file search.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
