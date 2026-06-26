## Description: <br>
Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to ask an agent to summarize web pages, local files, PDFs, images, audio, and YouTube links through the summarize CLI. It also helps configure model provider keys, output length, JSON output, extraction-only mode, and optional extraction fallbacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected files, URLs, or YouTube-derived content may be processed by the configured model provider or extraction provider. <br>
Mitigation: Use only organization-approved providers and avoid secrets, confidential documents, regulated data, and private URLs unless those services are approved for that data. <br>
Risk: Optional Firecrawl and Apify fallbacks can involve additional external processing. <br>
Mitigation: Disable optional fallbacks when they are not approved, such as using Firecrawl off and omitting Apify configuration. <br>


## Reference(s): <br>
- [Summarize homepage](https://summarize.sh) <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skill-0331-02) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and optional JSON output from the summarize CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summary length, maximum output tokens, extraction-only mode, JSON mode, Firecrawl fallback, YouTube fallback, and model provider configuration are exposed through CLI flags or config.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
