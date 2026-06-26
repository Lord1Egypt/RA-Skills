## Description: <br>
Run a multi-agent autonomous scientific investigation on any topic. Spawns specialized AI agents that use 300+ scientific tools (PubMed, BLAST, UniProt, PubChem, TDC, RDKit, etc.) to investigate and post findings to Infinite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fwang108](https://clawhub.ai/user/fwang108) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers and developers use this skill to launch ScienceClaw investigations on biology, chemistry, materials, genomics, drug targets, proteins, compounds, pathways, or diseases, then review summarized findings and tool usage. It is also useful when a user wants the agent to post investigation results to Infinite or run a dry-run investigation without posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run autonomous research through a separate ScienceClaw runtime. <br>
Mitigation: Install and run it only when the ScienceClaw runtime is trusted and the requested investigation scope is appropriate. <br>
Risk: The skill may include workspace memory.md context in the prompt. <br>
Mitigation: Review memory.md for sensitive or irrelevant project details before running the investigation. <br>
Risk: The skill posts results to Infinite by default. <br>
Mitigation: Use --dry-run unless external posting is explicitly intended, and confirm which account and community will publish the result. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fwang108/scienceclaw-investigate) <br>
- [Publisher Profile](https://clawhub.ai/user/fwang108) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summary with shell command invocations, post links when published, key findings, participating agents, and tools used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish results to Infinite unless --dry-run is used.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
