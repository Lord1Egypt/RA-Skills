## Description: <br>
Optimize RAG pipeline chunking strategy: analyze documents, recommend chunk sizes, splitting methods, overlap settings, and metadata enrichment for maximum retrieval quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to evaluate document corpora and choose chunking, overlap, metadata, and evaluation strategies for RAG pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RAG corpus analysis may expose private documents, metadata, or extracted text to external embedding providers. <br>
Mitigation: Run analysis only on documents intended for processing and review provider choices before sending private corpora or metadata outside the trusted environment. <br>
Risk: Chunking recommendations can reduce retrieval quality when applied without validation against representative queries. <br>
Mitigation: Evaluate proposed chunk sizes, overlap, and splitting methods with a representative query set before production rollout. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, configuration examples, analysis tables, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations depend on the provided corpus, embedding model, retrieval goals, and latency or storage constraints.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
