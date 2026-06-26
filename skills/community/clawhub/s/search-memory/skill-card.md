## Description: <br>
Local-first memory search and indexing for Openclaw. Use when you need to (1) index memory files, (2) search memory from the CLI, or (3) wire a slash command for memory lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Trumppo](https://clawhub.ai/user/Trumppo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to index local memory files and search them from the CLI with recency-aware keyword ranking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Indexing private notes can copy sensitive content into a local cache. <br>
Mitigation: Avoid indexing secrets or highly sensitive notes unless the local cache location and access controls are acceptable. <br>
Risk: The workflow invokes local scripts for indexing and search. <br>
Mitigation: Review and trust scripts/index-memory.py and scripts/search-memory.py before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance centers on local memory files, including MEMORY.md and memory/**/*.md, with cache output under memory/cache/.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
