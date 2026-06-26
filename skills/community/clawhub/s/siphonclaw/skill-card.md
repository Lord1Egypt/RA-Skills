## Description: <br>
Document intelligence pipeline with visual search, OCR, and field capture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[curtisgc1](https://clawhub.ai/user/curtisgc1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, field teams, and developers use SiphonClaw to ingest document collections, search them with text and visual retrieval, identify equipment or parts from photos, and capture field notes as reusable knowledge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users are asked to run external code and dependencies that may not have been independently reviewed. <br>
Mitigation: Review the repository and dependencies before running the skill, and start in a test environment. <br>
Risk: Document ingestion may process sensitive files through persistent storage, cloud APIs, web fallback, Telegram, email, or SSE channels. <br>
Mitigation: Ingest only deliberately selected non-sensitive documents at first, avoid broad home or shared-drive paths, and keep cloud, Brave Search, Telegram, email, and SSE access disabled until data handling and authentication controls are understood. <br>
Risk: Personal or production API keys could expose broader accounts or higher privileges than the skill needs. <br>
Mitigation: Use dedicated low-privilege API keys with budget limits and rotate them separately from production credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/curtisgc1/siphonclaw) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Model Context Protocol](https://modelcontextprotocol.io/) <br>
- [Ollama](https://ollama.ai) <br>
- [OpenRouter](https://openrouter.ai) <br>
- [Brave Search API](https://brave.com/search/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with JSON tool results, cited text answers, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return confidence scores, citations, ingestion status, model availability, and cost-tracking details.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
