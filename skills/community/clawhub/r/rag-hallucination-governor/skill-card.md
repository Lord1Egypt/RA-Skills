## Description: <br>
Diagnose and govern hallucination risk in production RAG systems with practical controls for retrieval thresholds, refusal or human handoff, citation coverage, Top1 pollution, conflict detection, and observability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[william202404](https://clawhub.ai/user/william202404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, AI engineers, and production support teams use this skill to triage RAG reliability failures where answers look plausible but rely on weak, wrong, conflicting, or out-of-scope evidence. It helps select concrete retrieval, reranking, citation, scope, refusal, and handoff controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Retrieval logs, citation spans, or permission context may contain customer or private business information. <br>
Mitigation: Use sanitized or appropriately authorized data when sharing logs or context with the skill. <br>
Risk: Incomplete retrieval evidence can lead to incorrect or overconfident triage guidance. <br>
Mitigation: Provide TopK chunks, scores, cited spans, scope fields, and handoff decisions when available; route unresolved conflicts or weak evidence to clarification or human review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/william202404/rag-hallucination-governor) <br>
- [Publisher profile](https://clawhub.ai/user/william202404) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown triage notes with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs identify trigger signals, production failure modes, control changes, metrics to watch, and refusal or human-handoff conditions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
