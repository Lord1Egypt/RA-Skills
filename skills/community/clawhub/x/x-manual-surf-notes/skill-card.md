## Description: <br>
Uses an attached logged-in X browser tab to scroll the For You feed, open posts, translate or summarize them into Chinese, deduplicate by status URL, and append structured Markdown notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaima2022](https://clawhub.ai/user/kaima2022) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to keep up with X For You posts, especially AI, tool, and product updates, while avoiding API scraping and maintaining a local Chinese notes file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent operates an attached logged-in X tab and can read the visible For You feed. <br>
Mitigation: Attach only the intended X tab, avoid unrelated sensitive pages in the browser relay, and stop the relay when the session is complete. <br>
Risk: The skill appends notes to a local Markdown file, which may use an undesired path if left unchanged. <br>
Mitigation: Review or change the output path before running the skill, then inspect appended notes before relying on them. <br>
Risk: Summaries and comments are derived from social posts and may reflect incomplete or unverified claims. <br>
Mitigation: Use the saved status links to verify important claims against the original post or cited source before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaima2022/x-manual-surf-notes) <br>
- [ClawHub listing text](artifact/references/listing.md) <br>
- [Browser scrape snippets](artifact/references/browser-scrape-snippets.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown notes appended to a local file with Time | Content | Link | Comment entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deduplicates entries by normalized X status URL; the default notes path is declared in the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
