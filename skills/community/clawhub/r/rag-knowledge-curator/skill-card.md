## Description: <br>
Curates enterprise documents for RAG pipelines by cleaning noisy text, chunking content, extracting metadata, scoring quality, and producing versioned ingestion recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boboy-j](https://clawhub.ai/user/boboy-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge engineers use this skill to prepare raw enterprise documents, web excerpts, and manuals for RAG ingestion by producing cleaner chunks, metadata, quality scores, and review recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pasted enterprise documents may contain sensitive information. <br>
Mitigation: Treat pasted documents as sensitive and review generated chunks before sending them to embedding or vector database pipelines. <br>
Risk: Generated chunks, metadata, quality scores, or ingestion recommendations may be incomplete or misleading if accepted without review. <br>
Mitigation: Review generated chunks and governance recommendations before ingestion. <br>
Risk: Credentials could be exposed if included in source documents or prompts. <br>
Mitigation: Keep credentials only in the external tools that perform ingestion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/boboy-j/rag-knowledge-curator) <br>
- [README](artifact/README.md) <br>
- [Input schema](artifact/schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown governance report with summary tables, chunk previews, metadata, quality scores, and optimization recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes user-provided text inputs; the README recommends inputs of 5000 characters or less per batch.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
