## Description: <br>
Extract decisions, todos, knowledge, preferences, and risks from AI chat sessions into structured memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, AI-assisted workers, and teams use this skill to turn one or more AI chat session logs into decisions, action items, reusable knowledge, preferences, risks, tags, summaries, and memory-ready exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session logs can contain secrets, private details, or sensitive business context. <br>
Mitigation: Review and redact transcripts before processing them with the skill. <br>
Risk: Memory-injection JSON can preserve false claims, private details, or prompt-injection content from the source session. <br>
Mitigation: Inspect memory-injection output before importing it into any long-term agent memory. <br>
Risk: Pattern-based extraction may miss context or promote partial snippets as decisions, preferences, or risks. <br>
Mitigation: Review generated archives before relying on them for onboarding, planning, or future agent context. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/session-archiver-pro) <br>
- [Session Archiver Pro Output Formats](references/formats.md) <br>
- [Publisher Profile](https://clawhub.ai/user/harrylabsj) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown reports, JSON documents, Obsidian-compatible Markdown notes, or memory-injection JSON printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can process a single file or a directory of .log, .txt, .json, and .md session logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
