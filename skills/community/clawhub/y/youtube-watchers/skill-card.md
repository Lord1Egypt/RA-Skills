## Description: <br>
Fetches YouTube transcripts for summarization and content extraction, and provides SkillBoss API examples for media generation, chat, search, document parsing, email, and SMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AbelTennyson](https://clawhub.ai/user/AbelTennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to fetch YouTube transcript content and to draft SkillBoss API calls for chat, media generation, search, document parsing, email, SMS, and related model tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad SkillBoss API access beyond YouTube transcript tasks, including paid model use and externally visible actions. <br>
Mitigation: Use a restricted or spending-limited API key when available, and require explicit confirmation before paid model calls or actions outside transcript retrieval. <br>
Risk: Email, SMS, scraping, document upload, audio upload, and media generation examples may send data to external services or contact third parties. <br>
Mitigation: Review destinations and inputs before execution, avoid sensitive data unless approved, and require confirmation before email, SMS, upload, scraping, or generation actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AbelTennyson/youtube-watchers) <br>
- [SkillBoss website](https://www.skillboss.co) <br>
- [SkillBoss API base URL](https://api.heybossai.com/v1) <br>
- [Chat Models](chat-models.md) <br>
- [Search and Scraping Models](search-models.md) <br>
- [Tool Models](tools-models.md) <br>
- [Audio Models](audio-models.md) <br>
- [Image Models](image-models.md) <br>
- [Video Models](video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for live API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
