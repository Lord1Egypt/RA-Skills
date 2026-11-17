## Description:

Design and build any search engine with robust indexing, retrieval logic, relevance controls, and evaluation workflows for production systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to design, evaluate, and safely roll out search systems for applications, documentation, product catalogs, or internal knowledge bases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local Markdown notes may contain sensitive project details if a user asks the skill to remember them.

Mitigation: Use session-only behavior when persistence is not wanted, and do not store API keys, passwords, legal identifiers, or private personal details in ~/search-engine/.

Risk: Search architecture or relevance guidance can be wrong for a specific workload without measured validation.

Mitigation: Validate indexing and relevance changes with benchmark queries, latency checks, rollback testing, and staged rollout gates before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/search-engine)
- [Search Engine Homepage](https://clawic.com/skills/search-engine)
- [Architecture Blueprint](artifact/architecture-blueprint.md)
- [Retrieval Patterns](artifact/retrieval-patterns.md)
- [Evaluation Metrics](artifact/evaluation-metrics.md)
- [Implementation Checklist](artifact/implementation-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Markdown planning notes under ~/search-engine/ when the user chooses persistent context.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
