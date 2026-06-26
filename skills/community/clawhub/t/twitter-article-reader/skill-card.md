## Description: <br>
Extract readable content from Twitter/X articles and tweets using jina.ai when a user provides a Twitter/X link and wants clean Markdown output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[showjim](https://clawhub.ai/user/showjim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch readable Markdown from public Twitter/X articles or tweets when direct Twitter/X pages are difficult to access or read. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided Twitter/X links are fetched through jina.ai, so the external service receives the URL. <br>
Mitigation: Use this skill only for public, non-sensitive Twitter/X links and avoid private, restricted, or confidential URLs. <br>
Risk: Extracted third-party social media content may be incomplete, unavailable, or changed at the source. <br>
Mitigation: Review the returned Markdown against the original public source when accuracy or completeness matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/showjim/twitter-article-reader) <br>
- [jina.ai reader endpoint](https://r.jina.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, API Calls] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns extracted article or tweet text with images preserved as Markdown image links when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
