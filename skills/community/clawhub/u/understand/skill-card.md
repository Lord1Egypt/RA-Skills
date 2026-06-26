## Description: <br>
Analyze a codebase to produce an interactive knowledge graph for understanding architecture, components, and relationships. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lum1104](https://clawhub.ai/user/Lum1104) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect a repository, identify source files and architectural layers, and generate an interactive knowledge graph with a guided tour of the codebase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads project source and can write a knowledge graph containing private architecture details. <br>
Mitigation: Run it only on repositories you are comfortable analyzing, and review or remove .understand-anything/ before sharing the project. <br>
Risk: The skill uses generated local helper scripts and repository commands during analysis. <br>
Mitigation: Use a trusted or contained workspace, especially for untrusted repositories, and review generated outputs before relying on them. <br>
Risk: Generated architecture, relationship, and tour content may be incomplete or misleading. <br>
Mitigation: Review the final graph and rerun with --full or a scoped directory when the repository changes or results look stale. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lum1104/understand) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance plus JSON knowledge graph files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes .understand-anything/knowledge-graph.json and .understand-anything/meta.json in the analyzed project.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
