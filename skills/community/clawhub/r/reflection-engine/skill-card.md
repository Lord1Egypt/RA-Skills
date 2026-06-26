## Description: <br>
Analyzes an AI agent's dream and knowledge graph data to surface the most frequent recurring DreamInsight themes from a knowledge_graph.json file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect recurring themes in an AI agent's DreamInsight knowledge graph and summarize what concepts appear most often. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The target knowledge_graph.json may contain private agent memory content. <br>
Mitigation: Inspect or sanitize the input file before running the skill, and run it only against a controlled memory location. <br>
Risk: The script uses hard-coded /home/albion/albion_memory paths and may create or open reflection.log despite declaring read-only permission. <br>
Mitigation: Edit the input and log paths to locations you control before execution, or disable logging if no log file should be written. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, analysis] <br>
**Output Format:** [Plain text printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Top 10 recurring dream themes with counts and a timestamp.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
