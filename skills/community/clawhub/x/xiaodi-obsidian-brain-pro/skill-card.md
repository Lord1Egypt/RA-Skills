## Description: <br>
Xiaodi Obsidian Brain Pro helps an agent turn WhatsApp or Telegram notes into Obsidian daily notes, apply terminology correction and redaction, search notes with local Ollama embeddings, and optionally sync the vault with Git. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mx6315909](https://clawhub.ai/user/mx6315909) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Obsidian users and developers use this skill to capture fragmented voice or chat notes, preserve them as Markdown daily notes, and retrieve related memories with local semantic search. It is aimed at private note workflows that need lightweight formatting, terminology cleanup, sensitive-data redaction, and optional Git backup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store and index sensitive personal notes. <br>
Mitigation: Use it only with a verified private Obsidian repository and review notes before enabling automated storage or indexing. <br>
Risk: Automatic Git sync can push private notes or insufficiently redacted content. <br>
Mitigation: Confirm the Git remote and repository visibility, disable or manually review auto-sync, and treat redaction rules as incomplete protection. <br>
Risk: The configured Ollama endpoint may not be the user's trusted local service. <br>
Mitigation: Change the Ollama endpoint to a trusted local address before running semantic search. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mx6315909/xiaodi-obsidian-brain-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes, shell commands, JSON configuration guidance, and plain-text search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local Obsidian Markdown files, query a configured Ollama endpoint, and run Git sync commands when enabled.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
