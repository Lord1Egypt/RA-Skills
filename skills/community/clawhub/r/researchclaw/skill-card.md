## Description: <br>
ResearchClaw orchestrates an autonomous research workflow from literature review and hypothesis generation through experiment execution, statistical analysis, paper drafting, peer review, and LaTeX export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongsheng123132](https://clawhub.ai/user/dongsheng123132) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and external users can use this skill to run a structured research pipeline that plans experiments, generates and executes code, analyzes results, drafts papers, and exports research artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The pipeline can execute generated experiment code locally or over SSH. <br>
Mitigation: Use only a trusted, pinned ResearchClaw implementation, start in simulated mode, inspect generated code before execution, and tightly scope any remote account, files, network access, and spending limits. <br>
Risk: Auto-approving gate stages can reduce human review before risky actions. <br>
Mitigation: Avoid --auto-approve for untrusted topics or environments and use manual gate approvals for stages that affect experiments, execution, or publication output. <br>
Risk: The skill requires LLM API credentials that could be exposed through configuration or runtime artifacts. <br>
Mitigation: Prefer environment-variable based credentials, protect the API key, and review generated artifacts before sharing them. <br>


## Reference(s): <br>
- [ResearchClaw ClawHub release](https://clawhub.ai/dongsheng123132/researchclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown instructions with bash and Python code blocks; pipeline outputs may include JSON, Markdown, LaTeX, Python code, and PNG charts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces staged run artifacts under an artifacts directory when the ResearchClaw pipeline is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
