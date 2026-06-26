## Description: <br>
SkillChain provides supply chain intelligence and ecosystem analysis for locally installed OpenClaw skills, including dependencies, categories, health, overlap, security posture, and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyx-cn](https://clawhub.ai/user/hyx-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use SkillChain to inventory local OpenClaw skills, map dependencies and tool usage, assess health and overlap, and generate ecosystem reports. Optional enrichment can add ClawHub popularity and moderation metadata when network access is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local scans can store skill metadata and local paths in the generated graph. <br>
Mitigation: Run scans only against directories intended for inspection and remove the generated graph when it is no longer needed. <br>
Risk: Optional online enrichment sends skill names to ClawHub to retrieve public popularity and moderation metadata. <br>
Mitigation: Skip the enrich command when network disclosure of local skill names is not appropriate. <br>
Risk: Broad scans of private folders can capture more local skill inventory information than intended. <br>
Mitigation: Use explicit scan directories for targeted audits instead of broad private folders. <br>


## Reference(s): <br>
- [SkillChain on ClawHub](https://clawhub.ai/hyx-cn/skill-chain) <br>
- [SkillChain Ontology Model](references/model.md) <br>
- [SkillChain Schema](schema/skillchain.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, terminal summaries, command examples, and append-only JSONL graph data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local skill graph metadata under memory/skillchain/graph.jsonl until removed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
