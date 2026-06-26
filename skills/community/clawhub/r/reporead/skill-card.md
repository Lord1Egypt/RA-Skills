## Description: <br>
Analyze GitHub repositories using RepoRead AI. Use when the user asks to "analyze a repo", "generate docs", "security audit a repo", "create a README", or wants AI-powered repository analysis. Supports MCP server integration and REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gdperkins](https://clawhub.ai/user/gdperkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to analyze public GitHub repositories with RepoRead for codebase orientation, documentation generation, security review, visual diagrams, and LLM-optimized summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends repository information to an external RepoRead analysis service. <br>
Mitigation: Use it only when RepoRead is an approved external service for the repository being analyzed, and avoid private or sensitive repositories unless explicitly approved. <br>
Risk: RepoRead analyses can consume account tokens. <br>
Mitigation: Check the token balance before starting analyses and confirm before queueing work that may spend tokens. <br>
Risk: The required API key could be exposed through shared logs or committed configuration. <br>
Mitigation: Use a dedicated, revocable REPOREAD_API_KEY and keep it out of committed files, transcripts, and shared logs. <br>


## Reference(s): <br>
- [RepoRead homepage](https://www.reporead.com) <br>
- [RepoRead public API](https://api.reporead.com/public/v1) <br>
- [RepoRead MCP endpoint](https://api.reporead.com/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/gdperkins/reporead) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration snippets, and API guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REPOREAD_API_KEY and curl for REST helper scripts; MCP server use is preferred when configured.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
