## Description: <br>
Recommends popular and high-quality Chinese RSS feeds from the top-rss-list project, with support for topic filtering, niche picks, OPML snippets, and feed-access troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weekend-project-space](https://clawhub.ai/user/weekend-project-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and RSS readers use this skill to find Chinese RSS feeds by popularity, topic, or niche quality and to generate concise OPML snippets for feed-reader import. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger terms such as top, AI, or news may activate the skill when RSS recommendations were not intended. <br>
Mitigation: Confirm the user's intent before providing a feed list when the request is ambiguous. <br>
Risk: Feed rankings, availability, and links may become stale or unreachable. <br>
Mitigation: Ask users to verify important feed links and treat generated OPML as a starting point for review before importing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weekend-project-space/top-rss-list) <br>
- [top-rss-list project](https://github.com/weekend-project-space/top-rss-list) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown tables, numbered lists, and OPML XML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Concise bilingual Chinese and English recommendations; no files or commands are produced.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
