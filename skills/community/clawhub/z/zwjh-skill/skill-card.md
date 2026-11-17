## Description:

zwjh-skill provides a local long-term memory, knowledge graph, retrieval, health audit, backup, and MCP access layer for agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fyniujin](https://clawhub.ai/user/fyniujin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to persist conversation and file knowledge locally, build a searchable memory graph, and expose query, deposit, health, export, and graph workflows to agents through CLI or MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memories may be exposed to other tools without the promised access controls being enforced.

Mitigation: Avoid enabling MCP access for lower-trust deployments until manifest and namespace checks are verified; restrict use to trusted local callers and review deposited memory contents.

Risk: The web UI may display stored values from untrusted deposited content.

Mitigation: Avoid using the web UI with untrusted memory content until stored values are rendered safely and reviewed.

Risk: Optional Baidu backup, external LLM adapters, CDN loading, and model or tokenizer downloads add separate network and data-sharing trust decisions.

Mitigation: Keep optional network features disabled unless the endpoint, token handling, and data-sharing implications have been reviewed.

Risk: Setup workflows can register scheduled tasks and write local memory, backup, and configuration files.

Mitigation: Review scheduled commands, storage paths, and backup targets before running setup, and run the skill under an account with only the required local permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fyniujin/skills/zwjh-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/fyniujin)
- [BAAI bge-small-zh-v1.5 ONNX model](https://huggingface.co/BAAI/bge-small-zh-v1.5/resolve/main/onnx/model_quantized.onnx)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI and MCP workflows may return plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may create or modify local memory stores, backups, schedules, graph exports, and MCP responses in the user's environment.]

## Skill Version(s):

2.6.0 (source: SKILL.md frontmatter, version.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
