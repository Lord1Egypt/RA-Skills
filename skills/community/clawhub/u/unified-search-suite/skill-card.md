## Description: <br>
Unified web search and deep research suite that routes ordinary queries to a deep search layer using Exa, Tavily, and Grok, while retaining legacy Tavily, Exa, and Google merged search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccmxigua](https://clawhub.ai/user/ccmxigua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run multi-provider web search, deep research, issue or thread tracing, and URL-to-Markdown extraction from an agent workflow. It is intended for lookup, fact-checking, source gathering, and document extraction tasks that can tolerate external search and parsing providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, snippets, URLs, and documents may be sent to external search or parsing providers. <br>
Mitigation: Use only non-confidential inputs unless provider routing and data handling have been reviewed for the deployment. <br>
Risk: Local credentials, including GitHub and search-provider tokens, may be read from the environment or OpenClaw credential files. <br>
Mitigation: Run with scoped credentials in an isolated environment and remove tokens that are not required for the selected workflow. <br>
Risk: Extraction workflows can create local artifacts containing fetched or parsed content. <br>
Mitigation: Review and clean generated workspaces or caches after processing sensitive URLs or documents. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ccmxigua/unified-search-suite) <br>
- [Report template](references/report-template.md) <br>
- [Vendored OpenClaw search skills README](vendor/openclaw-search-skills/README.md) <br>
- [Vendored OpenClaw search skills English docs](vendor/openclaw-search-skills/docs/README_EN.md) <br>
- [Search intent guide](vendor/openclaw-search-skills/search-layer/references/intent-guide.md) <br>
- [Content extraction heuristics](vendor/openclaw-search-skills/content-extract/references/heuristics.md) <br>
- [MinerU API docs](https://mineru.net/apiManage/docs) <br>
- [MinerU output files](https://opendatalab.github.io/MinerU/reference/output_files/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON summaries, shell command output, and extracted files depending on the selected search or extraction flow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source URLs, local artifact paths, extracted Markdown, consensus findings, uncertainty notes, and recommended next steps.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
