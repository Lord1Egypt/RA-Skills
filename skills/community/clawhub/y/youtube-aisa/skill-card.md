## Description: <br>
Search YouTube videos, channels, and playlists through the AISA YouTube endpoint with one API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search YouTube videos, channels, and playlists through AISA without managing Google API credentials. It supports query search, locale filters, pagination, and structured SERP-style results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: YouTube search queries and the AISA API key are sent to AISA's API. <br>
Mitigation: Use a scoped or easily rotated AISA_API_KEY, avoid sensitive search terms, and review AISA's privacy and retention practices before use. <br>
Risk: The skill depends on network access to api.aisa.one and a valid AISA_API_KEY. <br>
Mitigation: Run it only in trusted environments, provide the credential through environment variables, and review generated curl commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/youtube-aisa) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>
- [AISA YouTube search endpoint](https://api.aisa.one/apis/v1/youtube/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl command examples and structured API response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, network access to api.aisa.one, and AISA_API_KEY.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
