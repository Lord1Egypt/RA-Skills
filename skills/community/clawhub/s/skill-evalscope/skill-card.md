## Description: <br>
EvalScope translates natural language requests into evalscope CLI workflows for model accuracy evaluation, inference performance testing, RAG evaluation, visualization, benchmark discovery, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yunnglin](https://clawhub.ai/user/yunnglin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and evaluation engineers use this skill to turn requests about LLM quality, throughput, latency, RAG quality, embedding retrieval, and benchmark discovery into EvalScope commands, Python configuration, and troubleshooting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated dashboard commands can expose EvalScope result views if bound to a public interface. <br>
Mitigation: Bind dashboards to localhost unless there is an explicit network access requirement and the environment has appropriate access controls. <br>
Risk: Evaluation and RAG workflows may send private prompts, documents, datasets, or answers to model and embedding APIs. <br>
Mitigation: Use trusted endpoints and review provider retention terms before using sensitive datasets or credentials. <br>
Risk: Copied commands can include API keys or other sensitive credentials. <br>
Mitigation: Prefer environment variables or secret managers for credentials and remove keys from copied command text and logs. <br>
Risk: Code-generation benchmarks and sandbox evaluation can execute generated code. <br>
Mitigation: Run code benchmarks only in a hardened disposable sandbox, such as an isolated Docker environment with limited privileges and data access. <br>


## Reference(s): <br>
- [EvalScope ClawHub Skill Page](https://clawhub.ai/yunnglin/skill-evalscope) <br>
- [Eval Parameter Reference](artifact/eval-reference.md) <br>
- [Perf Parameter Reference](artifact/perf-reference.md) <br>
- [RAG Evaluation Reference](artifact/rag-reference.md) <br>
- [Examples](artifact/examples.md) <br>
- [Troubleshooting](artifact/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and Python configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include EvalScope CLI commands, Python RAGEval configuration, dashboard commands, benchmark lookup commands, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
