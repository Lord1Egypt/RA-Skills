## Description: <br>
Ingest articles, docs, notes, and web pages into a local LLM-WikiMind knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hal-9909](https://clawhub.ai/user/hal-9909) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-work users use this skill to save selected articles, documentation, notes, or web pages into a local WikiMind knowledge base. The skill helps classify content, write Markdown pages with frontmatter, update the search index, and log the ingest operation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent searchable records from selected content, including sensitive or private material if the user asks it to ingest that material. <br>
Mitigation: Avoid ingesting secrets, private conversations, or sensitive third-party content; use explicit prompts and review saved entries. <br>
Risk: The direct-file fallback writes Markdown files, updates the search index, and appends logs inside the configured WikiMind root. <br>
Mitigation: Keep WIKIMIND_ROOT pointed at the intended local knowledge base and review generated paths before relying on direct-file writes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hal-9909/wikimind-ingest) <br>
- [WikiMind skill homepage](https://github.com/HAL-9909/llm-wikimind-skill) <br>
- [LLM-WikiMind setup guide](https://github.com/HAL-9909/llm-wikimind#quick-start) <br>
- [Karpathy LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and frontmatter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local knowledge-base entries, index updates, and log entries when used with WikiMind.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
