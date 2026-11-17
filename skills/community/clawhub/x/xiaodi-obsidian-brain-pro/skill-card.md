## Description:

Turns WhatsApp or Telegram notes into Obsidian daily notes with local Ollama semantic search, speech-recognition term correction, and sensitive-data redaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mx6315909](https://clawhub.ai/user/mx6315909)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to capture fragmented voice or chat notes into Obsidian while preserving the user's original wording, correcting a small whitelist of misrecognized technical terms, and enabling local semantic retrieval through Ollama.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that the skill overreaches by reading agent memory and broad local note paths.

Mitigation: Review and constrain configured search paths before installation, and remove OpenClaw memory paths unless they are explicitly intended.

Risk: The security guidance warns that automatic Git push can send broad local repository changes to a network destination.

Mitigation: Disable or gate automatic Git push, confirm the remote repository is private and intended, and review pending changes before synchronization.

Risk: The security guidance flags the default Ollama endpoint as needing trust review.

Mitigation: Set Ollama to a trusted local loopback endpoint or another explicitly approved host before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mx6315909/skills/xiaodi-obsidian-brain-pro)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Organizer Prompt](artifact/prompts/organizer.txt)
- [Metadata](artifact/_meta.json)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown notes, file paths, shell command output, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local Obsidian note files, query a configured Ollama endpoint, and optionally trigger Git backup commands.]

## Skill Version(s):

1.1.4 (source: ClawHub server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
