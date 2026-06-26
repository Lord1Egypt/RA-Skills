## Description: <br>
Design and build any search engine with robust indexing, retrieval logic, relevance controls, and evaluation workflows for production systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to design, build, evaluate, and safely roll out search engines for applications, documentation, products, and internal knowledge bases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory may retain search-engine project context that the user did not intend to keep across sessions. <br>
Mitigation: Choose session-only use when persistence is unnecessary, and avoid storing secrets, credentials, legal identifiers, or sensitive business details in ~/search-engine/. <br>
Risk: User-approved external integrations for search infrastructure can send project data outside the local machine. <br>
Mitigation: Confirm the integration boundary before connecting services and limit shared data to the minimum needed for indexing, retrieval, or evaluation work. <br>
Risk: Indexing or relevance changes can regress search quality or production reliability if shipped without validation. <br>
Mitigation: Use offline benchmark comparisons, latency checks, staged rollout, monitoring, and rollback steps before expanding production traffic. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/search-engine) <br>
- [Skill Homepage](https://clawic.com/skills/search-engine) <br>
- [Architecture Blueprint](artifact/architecture-blueprint.md) <br>
- [Retrieval Patterns](artifact/retrieval-patterns.md) <br>
- [Evaluation Metrics](artifact/evaluation-metrics.md) <br>
- [Implementation Checklist](artifact/implementation-checklist.md) <br>
- [Setup](artifact/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with implementation plans, checklists, and optional code, shell command, or configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local notes under ~/search-engine/ when the user chooses persistent project context.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
