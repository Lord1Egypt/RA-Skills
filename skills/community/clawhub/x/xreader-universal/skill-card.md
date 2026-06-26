## Description: <br>
Universal content reader for WeChat/Bilibili/Twitter/YouTube/Xiaohongshu. Use when you need to fetch full article content from platforms that block simple HTTP fetching, especially WeChat public accounts. Supports: WeChat, Bilibili, X/Twitter, YouTube, Xiaohongshu, RSS, any web page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hoyaryyj](https://clawhub.ai/user/hoyaryyj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch article text, web-page content, feeds, and available video transcripts from platforms that block simple HTTP access. It is especially relevant for WeChat public-account articles and workflows that rely on a local x-reader CLI or Python library. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a separately installed local x-reader CLI that was not fully reviewed by the security evidence. <br>
Mitigation: Review the local x-reader installation before use and run it only in environments where you trust the installed package and its dependencies. <br>
Risk: Browser fallback and platform login workflows can save sessions for services such as Xiaohongshu or WeChat-related access. <br>
Mitigation: Use accounts and browser profiles appropriate for automation, understand where sessions are stored, and confirm you can revoke or remove them. <br>
Risk: The clear command removes inbox data without enough scope detail in the evidence. <br>
Mitigation: List and back up needed fetched content before clearing the inbox, and avoid running clear in shared or uncertain storage locations. <br>
Risk: Requested URLs or media may be sent to external retrieval or transcription services named in the artifact behavior. <br>
Mitigation: Avoid submitting sensitive, private, or restricted content unless those services are approved for the data involved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hoyaryyj/xreader-universal) <br>
- [Publisher profile](https://clawhub.ai/user/hoyaryyj) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, environment configuration, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce instructions that rely on an installed x-reader CLI, browser fallback sessions, and platform-specific content retrieval services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
