## Description: <br>
Build vector search with Weaviate using v4 syntax, proper module configuration, and production-ready patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to generate and review Weaviate v4 guidance for RAG, semantic search, module setup, batch imports, hybrid search, and index tuning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated examples may target the wrong Weaviate instance or production collection. <br>
Mitigation: Confirm the target Weaviate instance and test against non-production collections before running generated code. <br>
Risk: External vectorizer, generative, or reranker modules may send documents or queries to third-party AI providers. <br>
Mitigation: Enable only approved modules and avoid sending sensitive documents or queries to external AI providers without authorization. <br>
Risk: Module or API-key configuration errors can cause generated code to fail or produce empty results. <br>
Mitigation: Verify enabled Weaviate modules, required provider headers, and environment variables before execution. <br>


## Reference(s): <br>
- [Weaviate skill page](https://clawhub.ai/ivangdavila/weaviate) <br>
- [Module configuration](artifact/modules.md) <br>
- [Operations guide](artifact/operations.md) <br>
- [v3 to v4 migration reference](artifact/v4-syntax.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python, YAML, and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Weaviate v4 client examples, module settings, query patterns, batch import guidance, and debugging steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
