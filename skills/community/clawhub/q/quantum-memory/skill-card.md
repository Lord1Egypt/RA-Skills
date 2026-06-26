## Description: <br>
Quantum-enhanced long-term memory for AI agents - #1 on LongMemEval (98.6% R@5, 99.4% R@10, 0.9426 NDCG). Chunked gte-large retrieval with QAOA+CVaR subgraph optimization for agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dustin-a11y](https://clawhub.ai/user/dustin-a11y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add long-term memory, semantic recall, and optional graph-based retrieval refinement to AI agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored conversations may persist as sensitive long-term agent memory. <br>
Mitigation: Avoid storing credentials, personal data, or proprietary content until storage location, deletion behavior, and access controls are verified. <br>
Risk: The FastAPI server mode may expose memory endpoints if bound to untrusted interfaces. <br>
Mitigation: Confirm server binding, network exposure, and authentication or isolation controls before using it with real conversations. <br>
Risk: The skill depends on an external PyPI package to handle agent memory. <br>
Mitigation: Review and pin the package before deployment, and install it only in environments where third-party memory handling is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dustin-a11y/quantum-memory) <br>
- [GitHub project](https://github.com/Dustin-a11y/quantum-memory-graph) <br>
- [PyPI package](https://pypi.org/project/quantum-memory-graph/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installation and usage guidance for integrating a persistent memory package or FastAPI memory server with an agent.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
