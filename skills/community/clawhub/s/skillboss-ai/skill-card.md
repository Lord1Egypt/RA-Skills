## Description:

Skillboss gives agents access to 50+ AI models for image, video, audio, chat, search, document parsing, email, and SMS workflows, with smart routing for cost and quality preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yshuolu](https://clawhub.ai/user/yshuolu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use Skillboss to call or route across hosted AI models for chat, image, video, audio, search, document processing, email, and SMS tasks. It is useful when an agent needs one command-line wrapper for direct model calls, model discovery, or cost and quality based task routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, files, URLs, and generated outputs may be sent through SkillBoss and its providers.

Mitigation: Use only approved data, avoid sensitive audio or documents unless authorized, and confirm that the selected providers are acceptable for the task.

Risk: The SkillBoss API key is a secret and auth commands may expose it through stdout if logs are captured.

Mitigation: Store the key in a secret environment variable, avoid running auth commands in logged shells, and rotate the key if exposure is suspected.

Risk: Using --output can fetch returned media URLs automatically.

Mitigation: Save outputs only for trusted requests, review destination paths before execution, and inspect generated files before reuse.

Risk: Remote API responses are handled by the wrapper and may be incomplete, unexpected, or unsuitable for direct use.

Mitigation: Review generated text, files, and API responses before using them in downstream decisions or publishing workflows.

## Reference(s):

- [ClawHub Skillboss listing](https://clawhub.ai/yshuolu/skills/skillboss-ai)
- [Publisher profile](https://clawhub.ai/user/yshuolu)
- [SkillBoss website](https://www.skillboss.co)
- [SkillBoss API base](https://api.heybossai.com/v1)
- [API Integration](api-integration.md)
- [Error Handling](error-handling.md)
- [Chat Models](chat-models.md)
- [Image Models](image-models.md)
- [Audio Models](audio-models.md)
- [Video Models](video-models.md)
- [Search and Scraping Models](search-models.md)
- [Tool Models](tools-models.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance, shell commands, JSON API responses, text responses, and optional saved media or document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and SKILLBOSS_API_KEY; model outputs may include remote media URLs that can be downloaded when --output is used.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
