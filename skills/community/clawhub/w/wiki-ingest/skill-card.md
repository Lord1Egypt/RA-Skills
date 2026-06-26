## Description: <br>
Wiki Ingest helps an agent ingest a new source into a persistent markdown knowledge wiki by summarizing durable knowledge, updating relevant pages and links, and recording contradictions or open questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teki-ai](https://clawhub.ai/user/teki-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, writers, and teams maintaining Obsidian-friendly or git-backed markdown wikis use this skill to fold new articles, notes, reports, papers, transcripts, and meeting summaries into existing knowledge pages without creating unnecessary new pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may modify the wrong wiki files or introduce unwanted changes while updating markdown pages, index.md, or log.md. <br>
Mitigation: Limit the agent to the intended wiki folder and review diffs for page edits, index.md, and log.md before committing or syncing changes. <br>
Risk: Source ingestion can flatten uncertainty, contradictions, or speculative synthesis into the wiki. <br>
Mitigation: Keep source claims, existing wiki claims, and current synthesis distinct, and record contradictions, ambiguity, and follow-up questions explicitly. <br>


## Reference(s): <br>
- [Ingest Patterns](references/ingest-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown wiki updates, source summaries, index entries, log entries, and concise notes on contradictions or open questions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update source pages, topic pages, internal links, index.md, and log.md within the intended wiki.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
