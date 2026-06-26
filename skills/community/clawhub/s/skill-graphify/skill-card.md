## Description: <br>
Turn any folder of code, docs, papers, or images into a queryable knowledge graph. Cross-platform wrapper for graphify CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flobo3](https://clawhub.ai/user/flobo3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to map unfamiliar codebases or mixed project folders into a knowledge graph, then inspect generated reports, JSON, and interactive graph output to understand relationships across files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wrapper can install the unpinned graphifyy Python package at runtime. <br>
Mitigation: Install and run it in a virtual environment, and review the package source or pin an approved version before use in controlled environments. <br>
Risk: Generated graph, report, HTML, and cache files may contain indexed project content from the target folder. <br>
Mitigation: Run it only on folders appropriate for indexing, use .graphifyignore for secrets or private files, and review or delete graphify-out before sharing. <br>


## Reference(s): <br>
- [Graphify GitHub Repository](https://github.com/safishamsi/graphify) <br>
- [ClawHub Skill Page](https://clawhub.ai/flobo3/skill-graphify) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Python and CLI commands; generated artifacts include HTML, Markdown, JSON, and cache files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes graphify-out/graph.html, graphify-out/GRAPH_REPORT.md, graphify-out/graph.json, and graphify-out/cache/ under the target project.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
