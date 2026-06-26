## Description: <br>
Fetches URLs, extracts HTML content, generates summaries, and can cache results with configurable directory and TTL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudcompile](https://clawhub.ai/user/cloudcompile) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve public web pages, extract readable page text and metadata, summarize content, and return lightweight language, keyword, word-count, and read-time analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to user-provided URLs and stores fetched page content in a local cache. <br>
Mitigation: Use it for URLs whose network access and cached contents are acceptable, configure SITE_SUMMARIZER_CACHE_DIR and SITE_SUMMARIZER_CACHE_TTL for the environment, and clear the cache when handling sensitive material. <br>
Risk: Hiding the resolved IP in output does not hide the user's network identity from the destination server. <br>
Mitigation: Set SITE_SUMMARIZER_HIDE_IP when the resolved IP should not appear in output, and treat the destination request itself as visible network activity. <br>


## Reference(s): <br>
- [Site Summarizer on ClawHub](https://clawhub.ai/cloudcompile/site-summarizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [JSON object containing fetched content, summary, metadata, analysis, status, and cache fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local cache state and the resolved IP unless SITE_SUMMARIZER_HIDE_IP is enabled.] <br>

## Skill Version(s): <br>
4.1.0 (source: server release evidence and SKILL.md heading) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
