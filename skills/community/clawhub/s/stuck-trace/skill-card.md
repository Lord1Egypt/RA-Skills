## Description: <br>
Stuck Trace helps an agent analyze project, collaboration, or decision blocks by reading available user profile, memory, and recent conversation context, then producing a structured root-cause trace with decision points and possible paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sheyuy](https://clawhub.ai/user/sheyuy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this prompt skill when a real project, collaboration, or organizational decision feels blocked and they want the agent to map the structure of the blockage without giving advice or replacing the decision-maker. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read profile, memory, and recent conversation files, which can contain sensitive personal or workplace-confidential context. <br>
Mitigation: Run it only where the agent's accessible files are appropriate for analysis, keep highly sensitive records out of scope, and rely on the skill's output rules to avoid surfacing sensitive numbers, names, diagnoses, and private log content. <br>
Risk: Root-cause tracing can overstate patterns when memory evidence is sparse or incomplete. <br>
Mitigation: Use only supported observations, skip unsupported sections, avoid causal diagnoses, and clearly signal limited depth when memory or recent conversation history is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sheyuy/stuck-trace) <br>
- [Server-resolved GitHub provenance](https://github.com/Sheyuy/agent-skills/tree/main/skills/stuck-trace) <br>
- [Botlearn homepage](https://www.botlearn.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown with root-cause chain, decision-point, path, and reflection sections.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output depth adapts to available memory files and recent conversation context; the skill instructs the agent to avoid exposing sensitive numbers, names, medical details, and private log content.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
