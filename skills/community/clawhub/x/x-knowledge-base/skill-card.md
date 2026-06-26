## Description: <br>
Collects X bookmarks, fetches article content, enriches notes with optional AI summaries and cross-links, and stores them as an Obsidian knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hidicence](https://clawhub.ai/user/Hidicence) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to turn saved X bookmarks into local Markdown notes, enriched summaries, related-note links, and interest trend reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires raw X session credentials for the bird CLI. <br>
Mitigation: Use dedicated or revocable X credentials where possible, provide them only through environment variables, and verify the bird CLI source before running. <br>
Risk: Bookmark URLs and article content may be sent to third-party services such as Jina and MiniMax. <br>
Mitigation: Review bookmark sensitivity before processing, and leave MINIMAX_API_KEY unset when AI summaries are not required. <br>
Risk: Batch runs write Markdown notes and trend data into local bookmark and Obsidian directories. <br>
Mitigation: Set output directories explicitly and back up the Obsidian vault before running large batches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Hidicence/x-knowledge-base) <br>
- [Jina Reader endpoint used for article extraction](https://r.jina.ai/https) <br>
- [MiniMax API endpoint used for optional summaries](https://api.minimax.io/anthropic/v1/messages) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, terminal status text, and JSON trend data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes bookmark notes, cross-links, optional AI summary blocks, and local trend analysis files.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
