## Description:

Jasper Recall lets agents index, search, and recall private, shared, and learned memory using ChromaDB and SkillBoss API Hub embeddings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Jasper Recall to give agents searchable memory across prior sessions, daily notes, shared knowledge, and multi-agent collections. It supports recall, indexing, privacy checks, shared-memory sync, and optional automatic recall injection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private or sensitive memories may be exposed through recall results, shared collections, or automatic context injection.

Mitigation: Use public-only mode for sandboxed or untrusted agents, review memory tagging before sharing, run privacy checks on shared material, and disable autoRecall unless injected context is reviewed.

Risk: The HTTP recall server can expose indexed memory if it is bound beyond localhost or configured to allow private queries.

Mitigation: Keep the server bound to localhost, avoid public network exposure, and do not enable private query access on shared or public hosts.

Risk: Setup and recall flows execute local commands and may install dependencies.

Mitigation: Review commands before installation, avoid unpinned npx setup in privileged environments, and run the skill in a sandbox or dedicated account when handling sensitive memory.

Risk: Recall queries and indexed memory content may be sent to SkillBoss API Hub for embeddings.

Mitigation: Do not index or query secrets or highly sensitive records, and confirm that the API handling model is acceptable for the intended data before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/qui-jasper-recall)
- [Jasper Recall README](artifact/README.md)
- [Shared Memory Specification](artifact/docs/SHARED-MEMORY-SPEC.md)
- [Multi-Agent Mesh Guide](artifact/docs/MULTI-AGENT-MESH.md)
- [npm package](https://www.npmjs.com/package/jasper-recall)
- [Project repository listed in artifact metadata](https://github.com/E-x-O-Entertainment-Studios-Inc/jasper-recall)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, CLI output, JSON recall results, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for embedding-backed recall; memory recall may read local agent memory and selected shared collections.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact versions include SKILL.md 0.3.1, package.json 0.4.0, and CHANGELOG 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
