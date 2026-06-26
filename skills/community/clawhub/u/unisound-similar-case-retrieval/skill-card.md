## Description: <br>
医生端临床科研 — 相似病例语义检索与可解释排序，锚点病例对候选池做类比推理辅助。 <br>

This skill is for research and development only. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinicians, researchers, educators, and developers use this skill to compare a de-identified anchor clinical case against user-provided candidate case summaries, rank similar cases, and produce research-oriented explanations. It is intended for clinical research, teaching, and methodology discussion, not diagnosis or treatment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users could submit identifiable patient data to the disclosed medical LLM endpoint. <br>
Mitigation: Verify the endpoint and publisher, use approved de-identified inputs only, and confirm any required ethics or data-use approvals before running the skill. <br>
Risk: The generated case ranking and explanation could be mistaken for diagnosis or treatment advice. <br>
Mitigation: Treat the output as research and teaching assistance only, and require qualified clinical review before using any insight outside methodology discussion. <br>
Risk: The required app key could grant broader access than the skill needs. <br>
Mitigation: Use a least-privilege app key and rotate or revoke it according to local credential policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-similar-case-retrieval) <br>
- [Unisound-LLM publisher profile](https://clawhub.ai/user/unisound-llm) <br>
- [Medical LLM API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Analysis, Guidance] <br>
**Output Format:** [JSON object containing structured data and a Markdown explanation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ranks user-supplied candidate cases, echoes lightweight case metadata, and includes research-focused caveats.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
