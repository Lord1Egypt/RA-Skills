## Description: <br>
Accepts causal relationship graphs, detects cycle dependencies and dangling nodes, and returns repair suggestions for graph cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to submit causal graphs for cycle detection, dangling-node detection, repair suggestions, and health scoring before using the graph in downstream causal analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends causal graph data to an external Cloudflare-hosted service with limited disclosure about the operator and data handling. <br>
Mitigation: Do not submit private business logic, incident timelines, personal data, security investigations, or regulated information unless the operator and data handling are trusted. <br>
Risk: The public governance key is presented as a demo credential with unknown limits or permissions. <br>
Mitigation: Prefer a dedicated low-privilege key and confirm the key's scope before using the service in an agent workflow. <br>
Risk: Causal repair suggestions may be incorrect or misleading if the submitted graph is incomplete or encodes correlation as causation. <br>
Mitigation: Review suggested edge removals, classifications, and time-dimension changes before applying them to downstream causal analysis. <br>


## Reference(s): <br>
- [V19 Early Causal Graph Debugger on ClawHub](https://clawhub.ai/liuyanfeng1234/v19-early-causal-graph-debugger) <br>
- [Causal Graph Debugging API](https://boat-atlas-spa-flexible.trycloudflare.com/governance/causal-path-graph) <br>
- [V19 Trust Manifesto v1.1.0](https://clawhub.com/skills/v19-trust-manifesto) <br>
- [V19 Causal Dependency Analyzer](https://clawhub.com/skills/v19-causal-dependency-analyzer) <br>
- [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, Guidance, Shell commands] <br>
**Output Format:** [JSON responses with suggested shell commands in Markdown examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns detected cycles, dangling nodes, repair suggestions, and a graph health score.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
