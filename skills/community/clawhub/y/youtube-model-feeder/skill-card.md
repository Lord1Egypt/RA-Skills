## Description:

Food for your model - extract transcripts, key frames, OCR, slides, and LLM summaries from YouTube videos into structured AI-ready knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[celstnblacc](https://clawhub.ai/user/celstnblacc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and knowledge workers use this skill to turn YouTube videos into structured AI-ready notes with timestamped transcripts, captured frames, OCR text, slides, summaries, and Obsidian-ready exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned external Docker stack.

Mitigation: Review the referenced repository and Docker Compose configuration, pin a known commit, and confirm container mounts and exposed ports before installation.

Risk: Extracted video content may be sent to cloud LLM providers when OpenAI or Anthropic is selected.

Mitigation: Use the default local Ollama path for sensitive videos unless cloud processing is intentional, and verify provider credentials and settings before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/celstnblacc/skills/youtube-model-feeder)
- [Project Homepage](https://github.com/celstnblacc/youtube-model-feeder)
- [Obsidian Semantic Search](https://clawhub.ai/skills/obsidian-semantic-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, HTML, Obsidian bundle, API responses, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include timestamped transcript segments, image references, OCR text, slide captures, and LLM-generated summaries.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
