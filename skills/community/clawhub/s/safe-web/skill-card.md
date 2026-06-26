## Description: <br>
Safe-Web securely fetches URLs and searches web results by scanning retrieved content with PromptGuard for prompt injection threats before returning it to an agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdamNaghs](https://clawhub.ai/user/AdamNaghs) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use Safe-Web when untrusted web pages or search results need to enter an AI context window. It provides a safer command-line replacement for direct web fetch/search workflows by blocking or filtering content that PromptGuard identifies as suspicious. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Safe-Web depends on PromptGuard and local Python packages to decide whether retrieved content is safe. <br>
Mitigation: Review and trust the PromptGuard dependency and install dependencies in a virtual environment or user-local path where possible. <br>
Risk: A system-wide symlink or disabling native web tools can change browsing behavior for the local agent environment. <br>
Mitigation: Use the sudo symlink and native-tool disabling only when Safe-Web is intentionally meant to affect browsing workflows system-wide. <br>
Risk: Search uses the Brave Search API when BRAVE_API_KEY is configured. <br>
Mitigation: Provide the API key only in environments where sending search queries to Brave is acceptable. <br>


## Reference(s): <br>
- [Safe-Web on ClawHub](https://clawhub.ai/AdamNaghs/safe-web) <br>
- [PromptGuard dependency](https://clawhub.ai/seojoonkim/prompt-guard) <br>
- [Brave Search API](https://brave.com/search/api/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Plain text or JSON from command-line fetch and search operations, with optional saved text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses exit codes 0, 1, and 2 to distinguish clean output, operational errors, and blocked threats.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
