## Description:

Analyzes an AI agent's dream and knowledge graph to surface recurring themes from DreamInsight entities in a knowledge_graph.json file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to inspect a local knowledge graph and identify the most frequent themes in DreamInsight descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script reads a configured local knowledge_graph.json file and prints recurring concepts from DreamInsight descriptions, which may expose sensitive memory contents.

Mitigation: Run it only against knowledge graph files approved for inspection and review the printed terms before sharing output.

Risk: The artifact uses hardcoded /home/albion/albion_memory paths and has a minor log-file side effect.

Mitigation: Verify or edit the paths in tool.py before running, and remove or redirect the logging configuration if strictly read-only behavior is required.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text printed to standard output, with usage guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the top 10 recurring dream themes from the configured local knowledge_graph.json file.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
