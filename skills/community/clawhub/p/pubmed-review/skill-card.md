## Description: <br>
PubMed Review helps Feishu and OpenClaw users turn natural-language literature requests into PubMed searches, AI-generated brief and full reviews, notifications, and follow-up answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crayfish-ai](https://clawhub.ai/user/crayfish-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to request PubMed literature reviews from Feishu or the command line, generate structured summaries, store full Markdown reviews, and answer follow-up questions against prior PMID context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research content is sent to external MiniMax and PubMed services. <br>
Mitigation: Use a dedicated MiniMax key, allowlist the MiniMax and PubMed endpoints, and avoid confidential patient or unpublished project details. <br>
Risk: Shared task state can attach follow-up answers to the wrong review context. <br>
Mitigation: Require explicit task_id values or per-user context separation for follow-up answers on shared Feishu or OpenClaw hosts. <br>
Risk: Configurable endpoints, notification binaries, and environment files can expand execution risk on shared hosts. <br>
Mitigation: Pin or allowlist the MiniMax endpoint and notify executable, and keep environment files writable only by trusted administrators. <br>


## Reference(s): <br>
- [ClawHub PubMed Review release page](https://clawhub.ai/crayfish-ai/pubmed-review) <br>
- [PubMed E-utilities esearch endpoint](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi) <br>
- [PubMed E-utilities efetch endpoint](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi) <br>
- [MiniMax chat completion endpoint](https://api.minimax.chat/v1/text/chatcompletion_v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Feishu notification text, Markdown review files, JSON task records, and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Brief notifications are paired with full local Markdown reviews under results/pubmed; follow-up answers may cite PMID and article title context.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
