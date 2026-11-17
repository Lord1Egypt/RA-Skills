## Description:

Synapse Wiki helps an agent initialize, ingest into, query, and health-check a persistent Markdown wiki knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ankechenlab-node](https://clawhub.ai/user/ankechenlab-node)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and knowledge workers use this skill to create and maintain a local structured wiki from source notes, articles, papers, and project records. It supports recurring workflows for ingesting raw material, querying accumulated knowledge, and checking wiki health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation modifies the local Claude skills directory.

Mitigation: Install only from a trusted source and review the release contents before running the installer.

Risk: Wiki operations create and update persistent files under the wiki root supplied by the user.

Mitigation: Run commands only against an intended wiki directory and keep backups or version control for important knowledge bases.

Risk: Generated summaries, concepts, and query answers can contain incomplete placeholders or misleading synthesis.

Mitigation: Review generated Markdown before relying on it, publishing it, or promoting it into long-lived wiki pages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ankechenlab-node/skills/synapse-wiki)
- [Project homepage](https://github.com/ankechenlab-node/synapse-wiki)
- [Karpathy llm-wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, terminal text, shell commands, and generated local Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates files under the user-provided wiki root, including raw, wiki, log, and outputs paths.]

## Skill Version(s):

2.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
