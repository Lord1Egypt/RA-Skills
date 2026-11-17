## Description:

Fetches and summarizes recent arXiv and Hugging Face papers with Agentic Paper Digest for paper digests, JSON feeds, or local pipeline and API runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research-focused agents use this skill to configure and run an arXiv and Hugging Face paper digest workflow, then retrieve summarized papers through CLI JSON output or a local API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bootstrap process can run unpinned remote code from an upstream repository and install its dependencies.

Mitigation: Run bootstrap only in an isolated environment, and pin or verify the upstream repository and dependencies before installation.

Risk: The run scripts load .env as executable shell code, so a malicious or untrusted configuration file could execute commands or expose secrets.

Mitigation: Use only trusted .env files, avoid long-lived API keys, and keep unrelated secrets out of the runtime environment.

Risk: The API stop helper terminates processes on port 8000 and matching paper_finder server commands.

Mitigation: Use stop_api.sh only after confirming port 8000 is dedicated to this tool in the current environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quincygunter/skills/quincy-agentic-paper-digest-skill)
- [Agentic Paper Digest upstream project homepage from skill metadata](https://github.com/matanle51/agentic_paper_digest)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance]

**Output Format:** [Markdown guidance with shell command blocks and JSON-producing CLI/API outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, network access, and SKILLBOSS_API_KEY; can write a local SQLite data store under PROJECT_DIR.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
