## Description: <br>
Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users use this skill to summarize web pages, local files, PDFs, images, audio, and YouTube links through the summarize CLI. It is useful when an agent needs concise text or machine-readable summaries from user-selected sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URLs, documents, media, or extracted text selected for summarization may be processed by configured external AI providers or fallback extraction services. <br>
Mitigation: Use only approved providers for confidential, regulated, private, or customer data, and avoid submitting sensitive inputs unless organizational approval is in place. <br>
Risk: API keys and ~/.summarize/config.json can route data to different providers or optional services. <br>
Mitigation: Review configured API keys, selected model, and optional Firecrawl or Apify settings before using the skill in a controlled environment. <br>


## Reference(s): <br>
- [Summarize homepage](https://summarize.sh) <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skill-0327-04) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash examples; summarize CLI output may be plain text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports user-selected length, maximum output tokens, extract-only mode, provider model selection, and optional Firecrawl or Apify fallbacks.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
