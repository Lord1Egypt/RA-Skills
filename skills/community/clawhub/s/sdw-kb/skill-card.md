## Description:

Sdw Kb turns folders of code, docs, papers, images, and other content into a knowledge graph with clustered communities, interactive HTML, GraphRAG-ready JSON, and an audit report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangxiaoqiang1992](https://clawhub.ai/user/yangxiaoqiang1992)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and knowledge workers use this skill to turn local corpora into persistent knowledge bases, visualize concept relationships, query the graph, and export graph data for downstream tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scan and persist local folders, which may include secrets or sensitive corpora.

Mitigation: Run it only on intended directories, avoid confidential inputs, and review generated knowledge base files before sharing.

Risk: The skill installs and runs an unpinned Python package and can use optional external or long-lived integrations.

Mitigation: Review the package and commands before execution, constrain URLs and external services, and require explicit approval before Neo4j, MCP, watch, or URL-ingestion modes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangxiaoqiang1992/skills/sdw-kb)
- [uv installation documentation](https://docs.astral.sh/uv/getting-started/installation/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated artifacts can include HTML, JSON, Markdown, SVG, GraphML, Cypher, and Obsidian-compatible files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates self-contained knowledge base directories with graph outputs and audit reports.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
