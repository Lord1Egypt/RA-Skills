## Description: <br>
Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other external users use this skill to generate summaries of web pages, local documents, images, audio files, and YouTube videos through the summarize CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Summarized content may be sent to configured AI providers or optional extraction services. <br>
Mitigation: Avoid confidential documents, private URLs, regulated data, or sensitive media unless those providers and services are approved for that content. <br>
Risk: The skill depends on the externally installed summarize Homebrew package. <br>
Mitigation: Install only if the Homebrew package and configured providers are trusted in the deployment environment. <br>


## Reference(s): <br>
- [Summarize homepage](https://summarize.sh) <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skill-0327-01) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and optional JSON output from the CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The underlying CLI supports configurable summary length, maximum output tokens, extraction-only mode, JSON output, and optional Firecrawl or Apify fallback services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
