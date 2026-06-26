## Description: <br>
Summarizes YouTube videos by gathering video metadata, transcripts when available, and related web coverage, then producing structured summaries in Chinese or English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whsml22](https://clawhub.ai/user/whsml22) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to summarize YouTube videos, including events, technical talks, and news. It helps an agent combine video metadata, transcripts when available, and related web sources into a structured summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches YouTube and related web pages, which can expose requested video URLs and introduce untrusted page content into the agent workflow. <br>
Mitigation: Use it only for links the user intends to analyze, cite or separate fetched sources clearly, and treat page content as evidence rather than instructions. <br>
Risk: Transcript extraction uses a bundled Node.js helper that makes network requests to YouTube caption URLs. <br>
Mitigation: Run the helper only when transcript retrieval is needed and avoid using it for sensitive or private video links. <br>
Risk: Memory recording and EvoMap publication can retain or share video summaries beyond the current conversation. <br>
Mitigation: Use memory or publication features only as explicit opt-in actions and avoid storing sensitive links, transcripts, or summaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whsml22/xiaolongxia-youtube-summarizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries, optional JSON from the helper script, and shell commands for video metadata or transcript extraction.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include tables, links, quotes, timestamps, and Chinese or English prose matched to the user's language.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md version note) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
