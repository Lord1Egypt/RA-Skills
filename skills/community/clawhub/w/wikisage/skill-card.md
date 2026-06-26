## Description: <br>
A persistent plain-markdown LLM wiki that helps an agent ingest, query, lint, and maintain long-lived local knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harryzsh](https://clawhub.ai/user/harryzsh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill-aware agent users use Wikisage to keep a local markdown knowledge base current, answer questions from that knowledge base, and run health checks over wiki pages. It is intended for long-lived personal or team knowledge that should be curated with source and confidence annotations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists user-supplied knowledge and may store sensitive personal, customer, account, or decision records in the local wiki. <br>
Mitigation: Keep WIKI_ROOT private, scope access through the filesystem MCP allowed directory, and avoid storing secrets or regulated customer data. <br>
Risk: Broad ingest and lint workflows can modify multiple wiki pages, indexes, and logs. <br>
Mitigation: Review proposed ingest and lint changes before applying them, especially when the skill touches many pages. <br>
Risk: Optional embedding and notification workflows can send wiki-derived text or summaries to external cloud services, chat, email, or webhooks. <br>
Mitigation: Run embed.py and pipe lint summaries externally only when that data sharing is acceptable for the wiki contents. <br>


## Reference(s): <br>
- [Wikisage ClawHub listing](https://clawhub.ai/harryzsh/wikisage) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [mcporter](https://github.com/CrazyPython/mcporter) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and wiki file content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local markdown wiki pages, index entries, lint reports, logs, and optional embedding index operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
