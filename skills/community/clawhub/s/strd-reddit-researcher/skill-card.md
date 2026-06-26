## Description: <br>
Scans Reddit for posts matching keywords, summarizes findings, and supports research into communities, pain points, and user feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kryzl19](https://clawhub.ai/user/kryzl19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product researchers, and community analysts use this skill to search public Reddit discussions for keyword-matched posts and comments, then summarize themes, complaints, requests, and patterns into research reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research keywords, subreddit targets, and selected Reddit URLs are sent to external search and Reddit services. <br>
Mitigation: Avoid sensitive business plans, personal data, confidential topics, and any queries that should not be disclosed to those services. <br>
Risk: Cached results and exported Markdown reports can leave local copies of research topics and findings on disk. <br>
Mitigation: Remove cache and exported report files when the research should not remain on the machine. <br>
Risk: Search results and extracted summaries may be incomplete or misleading because they depend on external search responses, Reddit availability, and lightweight text extraction. <br>
Mitigation: Review the linked Reddit sources before using findings for product, security, legal, or business decisions. <br>


## Reference(s): <br>
- [ClawHub release: Reddit Researcher](https://clawhub.ai/kryzl19/strd-reddit-researcher) <br>
- [Publisher profile: kryzl19](https://clawhub.ai/user/kryzl19) <br>
- [Reddit JSON search endpoint](https://www.reddit.com/search.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown summaries, markdown export files, and terminal output with Reddit links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; accepts keyword, subreddit, and search-engine settings through arguments and environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
