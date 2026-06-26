## Description: <br>
Query the local knowledge base (OpenClaw docs, skills, internal wikis) using the QMD hybrid search engine (BM25 + Vector + LLM Re-ranking). Use this for technical questions about the agent's own capabilities, available skills, or documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pratiknarola](https://clawhub.ai/user/pratiknarola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to search a local QMD knowledge base for OpenClaw documentation, skill definitions, internal wiki content, and related technical answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries may surface sensitive or internal information from the local knowledge base. <br>
Mitigation: Use the skill only in environments where the local knowledge base is intended for agent access, and review retrieved content before sharing or acting on it. <br>


## Reference(s): <br>
- [QMD Knowledge Search on ClawHub](https://clawhub.ai/pratiknarola/qmd-knowledge-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands; JSON may be requested from qmd with --json.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Searches local QMD knowledge content and can filter results with --min-score.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
