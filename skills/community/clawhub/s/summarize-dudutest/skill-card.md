## Description: <br>
Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other external users use this skill to summarize web pages, local files, PDFs, images, audio, and YouTube links through the summarize CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send files, URLs, media, or extracted content to configured AI, extraction, or YouTube fallback providers. <br>
Mitigation: Avoid confidential files, private URLs, regulated data, and sensitive media unless the configured providers' data-handling terms are acceptable. <br>
Risk: The skill requires provider credentials and installs a CLI from a Homebrew package source. <br>
Mitigation: Use limited-scope API keys where possible and install only when the Homebrew package source and configured providers are trusted. <br>


## Reference(s): <br>
- [Summarize homepage](https://summarize.sh) <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/summarize-dudutest) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash command examples and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can control summary length, maximum output tokens, extraction-only mode, provider model, and optional Firecrawl or YouTube fallback services.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
