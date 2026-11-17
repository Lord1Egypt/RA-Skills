## Description:

Smart Code Search helps agents and developers find code and documentation by semantic meaning using local ColGREP and NextPlaid search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brettmhammond](https://clawhub.ai/user/brettmhammond)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to search unfamiliar codebases, locate implementations or patterns, and find related documentation when exact keywords or file paths are unknown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Indexing creates a local .colgrep/ directory that may be accidentally committed or created in the wrong project.

Mitigation: Run indexing only from the intended project directory and add .colgrep/ to .gitignore.

Risk: Agent integration commands modify local agent configuration to make ColGREP available as a search tool.

Mitigation: Run integration commands intentionally after reviewing the target agent and restart the agent only after setup is complete.

Risk: The rebuild command removes an existing local ColGREP index.

Mitigation: Use rm -rf .colgrep/ only when a full re-index is intended for the current project.

## Reference(s):

- [Advanced Usage & Architecture](references/advanced.md)
- [ColGREP and NextPlaid on GitHub](https://github.com/lightonai/next-plaid)
- [NextPlaid: Local-First Multi-Vector Database](https://lighton.ai/lighton-blogs/introducing-lighton-nextplaid)
- [LateOn-Code: ColGREP and LightOn](https://lighton.ai/lighton-blogs/lateon-code-colgrep-lighton)
- [The Bloated Retriever Era Is Over](https://lighton.ai/lighton-blogs/the-bloated-retriever-era-is-over)
- [Reason-ModernColBERT: Reasoning-Intensive Retrieval](https://lighton.ai/lighton-blogs/lighton-releases-reason-colbert)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ColGREP query examples, installation commands, indexing commands, and agent integration commands.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
