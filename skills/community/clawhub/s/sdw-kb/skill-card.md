## Description: <br>
Sdw Kb turns folders of code, documents, papers, images, and other content into a persistent knowledge graph with clustered communities, interactive HTML, GraphRAG-ready JSON, and an audit report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangxiaoqiang1992](https://clawhub.ai/user/yangxiaoqiang1992) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to index local folders into a navigable knowledge graph, inspect cross-document relationships, and generate reports and export files for graph-based analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently index local folders, which may capture sensitive repository or document content. <br>
Mitigation: Review the target path before running, use explicit /sdw-kb commands, and avoid indexing sensitive repositories unless the user has intentionally chosen them. <br>
Risk: Remote URL ingestion, Neo4j push, MCP server, watch mode, and hook installation can fetch content, transmit graph data, expose graph access to agents, or continue processing files over time. <br>
Mitigation: Enable add <url>, --neo4j-push, --mcp, --watch, and hook install only after reviewing their scope, destination, and persistence. <br>


## Reference(s): <br>
- [uv installation documentation](https://docs.astral.sh/uv/getting-started/installation/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with PowerShell commands plus generated HTML, JSON, GraphML, SVG, Cypher, and audit-report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written under a local knowledge-base directory and may include graph.html, graph.json, GRAPH_REPORT.md, cost.json, optional Neo4j Cypher, GraphML, SVG, Obsidian, MCP, and watch-mode artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
