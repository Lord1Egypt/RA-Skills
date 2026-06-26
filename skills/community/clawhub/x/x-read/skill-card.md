## Description: <br>
Render and summarize a public X (Twitter) link when you need to read the tweet/article content without logging in. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tylordius](https://clawhub.ai/user/tylordius) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
External users, developers, and agents use this skill to read publicly accessible X/Twitter permalinks and receive a concise Markdown summary of the tweet, thread replies, linked article content, links, timestamps, and media references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens public X links in Chromium with reduced browser isolation. <br>
Mitigation: Use trusted public X URLs only, avoid sensitive browsing contexts, and ask the publisher to remove the no-sandbox flags or clearly document why they are required. <br>
Risk: X page availability, login walls, or DOM changes can prevent extraction or produce incomplete summaries. <br>
Mitigation: Confirm important summaries against the original public link and retest the skill when X changes its page structure. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Skill Instructions](SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/tylordius/x-read) <br>
- [Publisher profile](https://clawhub.ai/user/tylordius) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Markdown thread summary with source URL, author, timestamp, extracted text, links, and media references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only output for public X/Twitter content; results depend on public page availability and current X page structure.] <br>

## Skill Version(s): <br>
1.0.1 (source: CHANGELOG, package.json, server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
