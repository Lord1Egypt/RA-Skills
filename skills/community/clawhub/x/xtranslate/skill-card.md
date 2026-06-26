## Description: <br>
Xtranslate helps agents translate PDF, Word, Excel, PowerPoint, TXT, and RTF documents while preserving document structure and supporting cloud, local Ollama, and built-in Python translation engines. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[GuoTao1980](https://clawhub.ai/user/GuoTao1980) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to translate individual documents or batches of documents across common office formats, choosing between cloud translation quality and local/offline processing for more sensitive files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud translation mode can send document contents to external or custom API endpoints. <br>
Mitigation: Use Ollama or another trusted local mode for confidential, legal, customer, or business-sensitive documents, and only configure custom endpoints that are explicitly trusted. <br>
Risk: Saved API-key encryption is not enough to protect valuable credentials on its own. <br>
Mitigation: Prefer environment variables or scoped, revocable keys, and run the skill in an isolated environment with least-privilege credentials. <br>
Risk: Batch folder translation can process more files than intended. <br>
Mitigation: Scope batch runs to narrow folders and review input and output paths before execution. <br>
Risk: Unpinned dependencies may change behavior or security posture over time. <br>
Mitigation: Install in an isolated environment and pin dependency versions before production or sensitive use. <br>


## Reference(s): <br>
- [Xtranslate ClawHub release page](https://clawhub.ai/GuoTao1980/xtranslate) <br>
- [Project Structure](artifact/references/project-structure.md) <br>
- [Naming Convention](artifact/references/naming-convention.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces translated documents in output folders and may create temporary conversion files and translation monitoring records.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
