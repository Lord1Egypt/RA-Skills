## Description: <br>
CLI tool for capturing and retrieving thoughts as a second brain, storing memories as daily markdown journals with optional semantic search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sorrycc](https://clawhub.ai/user/sorrycc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to help developers and CLI users initialize a segundo brain, capture journal entries, search or filter memories, and configure optional semantic search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal notes may be stored locally under ~/.segundo and can include sensitive content. <br>
Mitigation: Protect the ~/.segundo directory and avoid storing secrets or highly sensitive notes unless the user accepts that storage risk. <br>
Risk: Semantic search can use OpenAI cloud embeddings and API-key based processing. <br>
Mitigation: Prefer local Ollama embeddings for private notes, or use OpenAI only when cloud processing and API-key handling are acceptable. <br>
Risk: Suggested edit, delete, import, or export commands can change local memory files. <br>
Mitigation: Review commands before execution and keep backups or exports of important notes before destructive operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sorrycc/segundo) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose segundo CLI commands that read, write, edit, delete, import, or export local note files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
