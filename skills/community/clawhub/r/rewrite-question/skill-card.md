## Description: <br>
Rewrites user questions into self-contained queries by resolving conversational context, pronouns, time references, and omitted entities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LoveNerverMore](https://clawhub.ai/user/LoveNerverMore) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts can use this skill in conversational BI workflows to turn follow-up questions and ambiguous user queries into standalone questions before intent recognition or SQL generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Query text, conversation history, QA examples, and SQL templates may be sent to a configured LLM endpoint. <br>
Mitigation: Use only approved LLM endpoints, review GEMINI_API_URL, GEMINI_API_KEY, and GEMINI_TOKEN before use, and avoid sensitive data unless the endpoint is approved. <br>
Risk: Milvus retrieval and QA SQL templates can influence downstream SQL behavior. <br>
Mitigation: Review Milvus connection settings and validate matched SQL before using it in production workflows. <br>
Risk: The CLI --clean option deletes named workflow output files. <br>
Mitigation: Use --clean only when deleting rewrite_output.json and downstream workflow outputs is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LoveNerverMore/rewrite-question) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands] <br>
**Output Format:** [JSON object with a rewritten query, confidence score, rewrite flag, optional reasoning text, QA match flag, and optional SQL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When run from the CLI, writes rewrite_output.json in the shared workflow directory and can back up or clean named workflow outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
