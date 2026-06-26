## Description: <br>
Guide for designing and implementing a PostgreSQL database that fuses PageIndex-style document trees with LightRAG-style entity-relationship anchors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h4444433333](https://clawhub.ai/user/h4444433333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design PostgreSQL schemas, ingestion code, and retrieval SQL for hybrid tree-graph RAG systems. It is especially suited for converting nested PageIndex-style document trees into relational tables and anchoring LightRAG-style entities and relationships to tree nodes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents or extracted content may be stored in PostgreSQL or sent to a selected LLM extractor without the right data handling approval. <br>
Mitigation: Confirm that source documents may be stored and processed by the chosen database and LLM pipeline before adoption. <br>
Risk: Retrieval or ingestion examples may omit application-specific authorization constraints if copied directly. <br>
Mitigation: Preserve workspace and user authorization filters in all service-layer queries and review generated SQL before deployment. <br>
Risk: Example ingestion code could affect production data if run without validation. <br>
Mitigation: Test ingestion and retrieval changes against a staging PostgreSQL database before production use. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/h4444433333/tree-graph-rag) <br>
- [Integration Pattern](references/integration-pattern.md) <br>
- [Common Query Patterns](references/queries.md) <br>
- [PostgreSQL schema](references/schema.sql) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with SQL and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PostgreSQL DDL, ingestion logic, graph anchoring code, retrieval SQL, and concise design guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
