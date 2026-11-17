## Description:

SEEM stores and retrieves structured episodic memories for multi-turn conversations using fact graphs, PPR retrieval, hybrid dense and sparse retrieval, dynamic memory integration, and Lite, Pro, and Max recall modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryantoleco](https://clawhub.ai/user/ryantoleco)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use SEEM to preserve structured context across multi-turn conversations, retrieve relevant memories and facts, and control how much raw conversation context is returned to an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation content is stored on disk by default.

Mitigation: Keep the data directory private, avoid storing secrets or regulated data, and disable persistence or cache behavior when persistent local storage is not acceptable.

Risk: Persisted pickle files are auto-loaded and can execute code if tampered with.

Mitigation: Do not import or share persisted .pkl files, restrict write access to the data directory, and prefer a trusted local provider or disabled persistence until pickle persistence is replaced or otherwise controlled.

Risk: Conversation content is sent to configured LLM and embedding providers.

Mitigation: Use trusted providers, review provider data-retention terms, and configure local or approved endpoints for sensitive workloads.

## Reference(s):

- [SEEM ClawHub release page](https://clawhub.ai/ryantoleco/skills/seem-skill)
- [Publisher profile](https://clawhub.ai/user/ryantoleco)
- [Configured LLM API endpoint](https://api.deepseek.com)
- [Configured embedding API endpoint](https://api.siliconflow.cn/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, Python examples, shell commands, and structured memory result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recall output can include memory summaries, event structures, fact triples, raw chunks, backfilled context, scores, and multimodal references depending on the selected mode.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
