## Description:

Query the local knowledge base (OpenClaw docs, skills, internal wikis) using the QMD hybrid search engine (BM25 + Vector + LLM Re-ranking). Use this for technical questions about the agent's own capabilities, available skills, or documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratiknarola](https://clawhub.ai/user/pratiknarola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search and retrieve local OpenClaw documentation, skill definitions, internal wiki content, and QMD documentation when answering technical questions about available capabilities or documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may query or read a local knowledge base that contains internal wiki or capability documentation.

Mitigation: Confirm the agent is authorized to access /root/clawd/knowledge before installing or invoking the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pratiknarola/skills/qmd-knowledge-search)
- [Publisher profile](https://clawhub.ai/user/pratiknarola)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports optional JSON output from qmd commands when the agent adds --json.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
