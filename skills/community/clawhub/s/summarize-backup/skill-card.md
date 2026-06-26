## Description: <br>
Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bestrong1608-eng](https://clawhub.ai/user/bestrong1608-eng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and other users can use this skill to summarize selected web pages, local documents, images, audio files, and YouTube links through the summarize CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external summarize Homebrew package. <br>
Mitigation: Install the package only from a trusted source and review the package before use in managed environments. <br>
Risk: Summarized files, URLs, images, audio, videos, and fallback extraction requests may be processed by the selected AI provider or optional services. <br>
Mitigation: Avoid submitting confidential or private content unless the chosen provider and optional fallback services are approved for that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bestrong1608-eng/summarize-backup) <br>
- [Summarize homepage](https://summarize.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples; the underlying CLI may return text or JSON summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summary length, output token count, extraction-only mode, JSON output, Firecrawl fallback, YouTube fallback, model provider, and optional config file can be controlled through CLI flags or configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
