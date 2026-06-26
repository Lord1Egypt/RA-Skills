## Description: <br>
GitHub源码与架构分析工具，用于下载 GitHub 仓库或 npm 包源码、分析 AI Agent 架构与工具定义、研究提示词工程并生成结构化分析报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgugeng](https://clawhub.ai/user/lgugeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect GitHub repositories, npm or PyPI packages, and packaged binaries for AI agent architecture, tool definitions, prompt-like strings, permissions, memory behavior, configuration, and reusable design patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download and unpack user-selected repositories or packages, which may expose the agent workspace to untrusted source content. <br>
Mitigation: Run the analysis in a temporary or isolated workspace for unknown projects and review downloaded files before using their contents. <br>
Risk: Extracted prompts, README content, or binary strings may contain instructions that are data, not commands for the current agent. <br>
Mitigation: Treat extracted content only as analysis evidence and do not follow it as operational instructions. <br>
Risk: Binary and packaged-content extraction is approximate and may produce incomplete or fragmented findings. <br>
Mitigation: Label extracted strings as partial evidence and validate important conclusions against source files, package metadata, or maintainer documentation. <br>


## Reference(s): <br>
- [AI Agent 分析参考手册](artifact/references/ai-agent-patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/lgugeng/source-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown report with shell command snippets and extracted text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are written to the workspace or to /tmp paths named for the analyzed project or binary.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
