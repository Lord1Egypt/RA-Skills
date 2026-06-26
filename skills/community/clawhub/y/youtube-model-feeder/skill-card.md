## Description: <br>
Food for your model - extract transcripts, key frames, OCR, slides, and LLM summaries from YouTube videos into structured AI-ready knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[celstnblacc](https://clawhub.ai/user/celstnblacc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to turn YouTube tutorials and talks into searchable transcript, screenshot, OCR, slide, and summary bundles for AI assistants or Obsidian workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow relies on external Docker code and a docker-compose stack. <br>
Mitigation: Inspect the referenced repository and docker-compose file before installation, confirm it is the intended source, and do not use force install only to bypass a warning. <br>
Risk: Video transcripts, OCR text, screenshots, and summaries may be sent to OpenAI or Anthropic when those providers are selected. <br>
Mitigation: Use local Ollama for sensitive videos; when using hosted providers, assume video-derived content is sent to that provider. <br>
Risk: Generated database records, screenshots, ZIP exports, Obsidian notes, and API keys may persist after use. <br>
Mitigation: Track generated content and credentials, then remove exported content or API keys when no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/celstnblacc/youtube-model-feeder) <br>
- [Source Repository](https://github.com/celstnblacc/youtube-model-feeder) <br>
- [Obsidian Semantic Search](https://clawhub.ai/skills/obsidian-semantic-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated knowledge bundles in Markdown, HTML, or ZIP form] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create transcript segments, screenshots, OCR text, slide captures, summaries, database records, and Obsidian-ready exports.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
