## Description: <br>
Repo Explainer turns a public GitHub repository or local code directory into source-grounded HTML and Markdown reports that explain purpose, architecture, modules, flows, dependencies, and limitations for non-developers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoloyyh](https://clawhub.ai/user/yoloyyh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, PMs, designers, and managers use this skill to understand what a repository or local codebase does, how it is built, and where key evidence appears in source files. It is useful for onboarding, technical discovery, and creating shareable codebase summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent reads the repository or local folder supplied for analysis, which may expose sensitive private code to the active agent and LLM environment. <br>
Mitigation: Use it only on repositories or folders approved for that environment, and avoid sensitive private code unless internal data-handling requirements are met. <br>
Risk: Reruns may replace the generated workspace clone folder used for analysis. <br>
Mitigation: Do not store important manual work inside the generated workspace clone path; keep source work in its original repository or another durable location. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yoloyyh/repo-explainer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [HTML and Markdown reports with source citations and Mermaid diagrams] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces synchronized report files for public GitHub repositories or local code directories; evidence links are commit-pinned when GitHub coordinates are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
