## Description:

Efficient Lifelong Memory for LLM Agents - semantic compression, cross-session memory, and intent-aware retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nantes](https://clawhub.ai/user/nantes)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to add persistent SimpleMem-backed memory storage, synthesis, and retrieval to OpenClaw-style agents, with a JSON fallback when full SimpleMem features are unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists memory content on disk, including the bundled local JSON fallback store.

Mitigation: Do not store secrets, credentials, regulated personal data, or confidential business content as memories; review or delete artifact/data/memories.json when clearing local memory.

Risk: When OPENAI_API_KEY is enabled, memory and query text may be processed outside the local machine by SimpleMem or OpenAI-backed services.

Mitigation: Enable the API key only when that data flow is acceptable, and avoid sending sensitive memory content through the semantic path.

Risk: Installing the SimpleMem dependency from a package or repository introduces normal third-party dependency supply-chain risk.

Mitigation: Use a pinned dependency version or reviewed commit before deployment.

## Reference(s):

- [SimpleMem GitHub Repository](https://github.com/aiming-lab/SimpleMem)
- [SimpleMem Paper](https://arxiv.org/abs/2601.02553)
- [Simplemem ClawHub Skill Page](https://clawhub.ai/nantes/skills/simplemem)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline PowerShell, Python, and shell command examples; runtime retrieval returns text memory results and simple statistics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python for local execution. OPENAI_API_KEY enables full SimpleMem-backed features; without it, the wrapper uses local JSON storage and keyword search.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
