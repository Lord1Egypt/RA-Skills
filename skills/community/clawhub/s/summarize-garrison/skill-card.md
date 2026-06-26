## Description: <br>
Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[securecloudprojo](https://clawhub.ai/user/securecloudprojo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other users use this skill to ask an agent to summarize web pages, local files, PDFs, images, audio, and YouTube links through the summarize CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Summarization may send local files, private URLs, or extracted content to configured AI and extraction providers. <br>
Mitigation: Avoid confidential inputs unless the configured providers' data-handling terms are acceptable; use scoped API keys where possible. <br>
Risk: The skill depends on the external summarize CLI and Homebrew formula supply chain. <br>
Mitigation: Install only when the publisher and Homebrew formula are trusted, and review the formula before deployment. <br>
Risk: Configured providers and fallback extraction services can incur usage-based costs. <br>
Mitigation: Monitor provider billing and limit API key scope or access for routine use. <br>


## Reference(s): <br>
- [Summarize homepage](https://summarize.sh) <br>
- [ClawHub skill page](https://clawhub.ai/securecloudprojo/summarize-garrison) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can request JSON output from the summarize CLI and configurable summary lengths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
