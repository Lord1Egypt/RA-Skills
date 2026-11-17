## Description:

Supply chain intelligence and ecosystem analysis for OpenClaw skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyx-cn](https://clawhub.ai/user/hyx-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use SkillChain to inventory local OpenClaw skills, map tool, package, and skill relationships, check security posture and health, detect overlap, and generate ecosystem reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inventories local skill directories and stores graph metadata about discovered skills.

Mitigation: Run scans only against directories intended for analysis and review the generated graph before sharing it.

Risk: Online enrichment can query installed skill slugs against clawhub.ai.

Mitigation: Use enrichment deliberately and skip it when local skill inventory names should remain local.

Risk: The package can automatically import and execute a sibling ontology Python module when present.

Mitigation: Review the sibling ontology skill before use or run SkillChain in an isolated workspace without that sibling skill installed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hyx-cn/skills/skill-chain)
- [SkillChain Ontology Model](references/model.md)
- [SkillChain Schema](schema/skillchain.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; scripts can produce text reports, Markdown reports, and local JSONL graph data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional online enrichment queries public ClawHub metadata when network access is available.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
