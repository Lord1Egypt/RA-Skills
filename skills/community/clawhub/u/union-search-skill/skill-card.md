## Description: <br>
Provides a unified command-line search interface across developer communities, social platforms, general search engines, AI search providers, RSS feeds, URL-to-Markdown conversion, and multi-platform image search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runningZ1](https://clawhub.ai/user/runningZ1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run searches across many web, social, developer, media, and image sources through a common CLI, then return structured results or archived responses for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch and download web content from many external sources. <br>
Mitigation: Install and run it only in workspaces where broad web retrieval is acceptable, and review downloaded or fetched content before reuse. <br>
Risk: Some integrations may use local credentials, API keys, browser cookies, or account cookies. <br>
Mitigation: Use least-privilege credentials, avoid account cookies unless necessary, and rotate or remove secrets after testing. <br>
Risk: Server security evidence reports a hardcoded SerpAPI key. <br>
Mitigation: Remove or replace the hardcoded key before use and provide secrets through managed environment variables. <br>
Risk: Search logs and archived responses may retain sensitive queries or retrieved content. <br>
Mitigation: Disable logging when not needed, store logs outside sensitive directories, and delete retained responses according to the user's data-handling policy. <br>
Risk: Server security evidence identifies a command-injection-prone legacy Exa mcporter helper. <br>
Mitigation: Do not use that helper until the shell invocation is fixed and reviewed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/runningZ1/union-search-skill) <br>
- [README](README.md) <br>
- [API credential guide](references/api_credentials.md) <br>
- [Rate limits](references/rate_limits.md) <br>
- [Platform notes](references/platform_notes.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Google search guide](references/google_search_guide.md) <br>
- [Baidu API key guide](references/baidu_apikey_fetch.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown, JSON, terminal text, saved response files, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save raw API responses and search logs when enabled by the invoked scripts.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
