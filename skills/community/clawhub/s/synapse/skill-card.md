## Description:

Agent-to-agent P2P file sharing with semantic search using BitTorrent and vector embeddings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pendzoncymisio](https://clawhub.ai/user/pendzoncymisio)

### License/Terms of Use:


## Use Case:

Developers and agent operators use Synapse to share files or memory shards over a BitTorrent-based peer-to-peer network and discover them by semantic similarity. It supports sharing, searching, downloading, seeding, and optional memory-shard validation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can share local files and memory shards over peer-to-peer networks, which can expose sensitive content if the wrong paths are selected.

Mitigation: Use the skill only in a contained environment and review file paths before sharing; do not share sensitive files.

Risk: The default tracker and tracker examples include public HTTP endpoints, so metadata and discovery traffic may be visible outside the local machine.

Mitigation: Prefer HTTPS or private trackers and treat tracker registration data as public.

Risk: Assimilation can skip safety checks, which may allow unsafe downloaded content to be integrated into agent memory.

Mitigation: Do not use the safety-skip option; keep validation and safety scanning enabled before memory ingestion.

Risk: The background seeder uses a local control socket and the security evidence warns that current socket permissions and handler templating are weak.

Mitigation: Do not run the background seeder on a multi-user system until socket permissions and command templating are fixed.

## Reference(s):

- [Synapse README](README.md)
- [Synapse Installation and Usage](SKILL.md)
- [SynapseTracker Server](https://github.com/Pendzoncymisio/SynapseTracker)
- [ClawHub Skill Page](https://clawhub.ai/pendzoncymisio/skills/synapse)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and CLI output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce magnet links, tracker search results, local seeder status, and configuration values for peer-to-peer file sharing workflows.]

## Skill Version(s):

0.2.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
