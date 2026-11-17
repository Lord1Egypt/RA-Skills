## Description:

This skill maintains the Note Embeddings for Zettelkasten, to search notes, retrieve notes, and discover connections between notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hxy9243](https://clawhub.ai/user/hxy9243)

### License/Terms of Use:


## Use Case:

Developers and note-takers use this skill to configure embeddings for an Obsidian or Markdown note directory, search notes semantically, and discover related notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote provider mode can send note text and search queries off-device to OpenAI or Gemini.

Mitigation: Prefer the default local Ollama provider for sensitive notes, and use remote providers only with explicit consent and limited API keys.

Risk: Embedding caches, note previews, search results, and discovered links are stored under .embeddings.

Mitigation: Run the skill only on intended Markdown directories and treat .embeddings as sensitive output that should not be shared or committed without review.

Risk: Mutable install commands or unverified provider URLs can change what code or endpoint is used.

Mitigation: Pin the installer and source revision where possible, and verify remote provider URLs use expected HTTPS endpoints before embedding notes.

## Reference(s):

- [Zettel Link on ClawHub](https://clawhub.ai/hxy9243/skills/zettel-link)
- [Ollama](https://ollama.com)
- [OpenAI API](https://platform.openai.com/)
- [Google AI for Developers](https://ai.google.dev/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, json, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes embedding caches, search results, and link discovery files under the configured .embeddings directory.]

## Skill Version(s):

1.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
