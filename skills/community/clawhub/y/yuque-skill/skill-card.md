## Description: <br>
语雀 Skill lets agents manage Yuque documents and knowledge bases through the Yuque API, including document CRUD, TOC changes, Markdown formatting, search, and batch import/export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feixuelingcloud](https://clawhub.ai/user/feixuelingcloud) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and knowledge-base maintainers use this skill to let an agent publish, update, search, export, import, and reorganize Yuque documentation with authenticated API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live authenticated changes to Yuque documents and knowledge-base structure. <br>
Mitigation: Use a dedicated least-privilege Yuque token and explicitly confirm write operations before running scripts that create, update, move, import, or replace content. <br>
Risk: Delete and TOC remove operations can remove documents or detach them from the knowledge-base structure. <br>
Mitigation: Require explicit confirmation for delete and TOC remove operations, and use `--keep-doc` when removing TOC nodes unless the underlying document should also be deleted. <br>
Risk: Bulk import and non-dry-run replacement can affect many documents at once. <br>
Mitigation: Run bulk replacements with `--dry-run` first, review the affected count and examples, and keep a local export before applying broad changes. <br>


## Reference(s): <br>
- [语雀 Skill on ClawHub](https://clawhub.ai/feixuelingcloud/yuque-skill) <br>
- [API Reference](references/api_reference.md) <br>
- [Markdown Format Guide](references/markdown_format.md) <br>
- [TOC Operations Guide](references/toc_operations.md) <br>
- [Yuque API Documentation](https://www.yuque.com/yuque/developer/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON results from scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce live Yuque API changes when valid credentials are configured.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
