## Description:

semantic-split turns natural-language requests into structured JSON planning blocks using regex structure analysis, BGE semantic matching, reranking, 5W2H extraction, constraint annotation, and gated planning steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldxs001](https://clawhub.ai/user/ldxs001)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to split natural-language work requests into structured requirement blocks, planning steps, work-package decomposition, and reusable JSON templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network installs and model downloads can introduce package and model supply-chain risk.

Mitigation: Review dependencies and model sources before running auto-install or model-download commands; install in an isolated environment with approved packages and model sources.

Risk: Broad triggers, template scanning, and historical memory processing can expose sensitive or unrelated data.

Mitigation: Select exact files and directories for scanning, apply redaction rules, and avoid granting access to broad memory paths.

Risk: Persistent JSON template writes can preserve incorrect, sensitive, or low-quality plans.

Mitigation: Review generated JSON before saving or reusing it and limit write access to the skill's data directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ldxs001/skills/semantic-split)
- [FlagEmbedding project](https://github.com/FlagOpen/FlagEmbedding)
- [Attribution](references/attribution.md)
- [JSON schema](references/json_schema.md)
- [Loading decision tree](references/loading_decision_tree.md)
- [Planning rules](references/planning_rules.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [JSON objects and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include structured requirement blocks, 5W2H fields, constraint annotations, step lists, work-package decomposition, hook status, and reusable template JSON.]

## Skill Version(s):

3.1.1 (source: frontmatter, _meta.json, release evidence, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
