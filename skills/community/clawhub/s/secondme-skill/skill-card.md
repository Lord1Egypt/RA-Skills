## Description: <br>
A complete pipeline to build your AI Second Me: distill your identity from personal data, grow a private knowledge base, train a local model, and govern what gets shared. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neiljo-gy](https://clawhub.ai/user/neiljo-gy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, maintainers, and end users use this skill to orchestrate a local-first personal AI persona pipeline across data ingestion, identity distillation, knowledge management, model training, evaluation, integration, and release reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive personal data while creating persona, knowledge, and model artifacts. <br>
Mitigation: Use a dedicated workspace, authorize only specific source folders, keep local-first defaults, and require explicit approval before external sharing. <br>
Risk: External interoperability features such as ACN, A2A, on-chain integration, and external sharing may expose identity artifacts beyond the local workspace. <br>
Mitigation: Disable or tightly gate external interoperability unless it is intentionally needed, and audit any export or sharing action. <br>
Risk: Generated persona and model artifacts can be promoted before quality gates are satisfied. <br>
Mitigation: Run the bundled gate scripts and keep report or deployment recommendations blocked unless data, training, quality, governance, sync, model integration, and publish checks pass. <br>


## Reference(s): <br>
- [Product Report](references/product-report.md) <br>
- [Report Template](references/report-template.md) <br>
- [Submission Split Checklist](references/submission-split.md) <br>
- [ACN Gateway](https://acn-production.up.railway.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration references, and report file conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces staged pipeline instructions and gated report artifacts under reports/data, reports/model, and reports/deploy.] <br>

## Skill Version(s): <br>
0.1.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
