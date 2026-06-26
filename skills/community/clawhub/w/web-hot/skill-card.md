## Description: <br>
Fetches real-time hot search lists and trending topics from major Chinese platforms including Weibo, Zhihu, Baidu, Douyin, Toutiao, and Bilibili. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lk360287680-byte](https://clawhub.ai/user/lk360287680-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve and summarize current trending topics across major Chinese social media, search, news, and video platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts the third-party 60s.viki.moe API to retrieve live public trend lists. <br>
Mitigation: Install it only where outbound access to that API is acceptable and avoid using it for sensitive private research. <br>
Risk: Returned topics and links are third-party web content and may be inaccurate, stale, or unsuitable for a given audience. <br>
Mitigation: Treat returned content as untrusted external information and review results before relying on or sharing them. <br>


## Reference(s): <br>
- [60s API Documentation](https://docs.60s-api.viki.moe) <br>
- [60s API Base](https://60s.viki.moe/v2) <br>
- [ClawHub Skill Page](https://clawhub.ai/lk360287680-byte/web-hot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with JSON API examples and Python or Bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live public data from the 60s.viki.moe API; no credentials are requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
