## Description: <br>
This skill maintains note embeddings for Zettelkasten workflows to search notes, retrieve notes, and discover connections between notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hxy9243](https://clawhub.ai/user/hxy9243) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, note-takers, and knowledge-management users use this skill to configure embeddings, index Markdown notes, run semantic search, and find related notes in an Obsidian-style vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote embedding providers can receive note text and search queries when OpenAI or Gemini is selected. <br>
Mitigation: Use the default local Ollama provider for private vaults, or switch providers only after confirming that sending note content and queries to that service is acceptable. <br>
Risk: The .embeddings cache stores derived note data after indexing. <br>
Mitigation: Review or delete the .embeddings cache when the derived note data is no longer needed. <br>
Risk: API keys may be loaded from a local .env file for remote providers. <br>
Mitigation: Keep .env files out of synced note folders and source control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hxy9243/zettel-link) <br>
- [Ollama](https://ollama.com) <br>
- [OpenAI API](https://platform.openai.com/) <br>
- [Google Gemini API](https://ai.google.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and reads local embedding caches under .embeddings, including embeddings.json, search_results.json, and links.json.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
