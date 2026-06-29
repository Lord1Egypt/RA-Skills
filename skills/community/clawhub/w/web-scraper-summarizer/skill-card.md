## Description: <br>
Fetches web pages and generates AI-powered summaries using an Ollama LLM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and other users use this skill to fetch public web pages and generate brief, detailed, or bullet summaries with a local Ollama LLM. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetching user-provided URLs can expose internal or confidential page content to the local Ollama setup and command output. <br>
Mitigation: Use the skill for public web pages or approved URLs only, and avoid internal, private, or sensitive content. <br>
Risk: Source pages may contain adversarial instructions or misleading content that affects generated summaries. <br>
Mitigation: Treat summaries as untrusted, verify important claims against the source page, and review results before relying on them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text summaries printed to stdout, with progress and errors on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports brief, detailed, and bullet summary styles; page text is truncated before summarization; raw content may be printed if Ollama fails.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
