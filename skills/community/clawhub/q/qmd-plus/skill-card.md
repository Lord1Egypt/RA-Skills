## Description: <br>
Enhanced QMD search with LLM-powered query expansion for improving recall and precision across multilingual markdown knowledge bases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thehappyboy](https://clawhub.ai/user/thehappyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-base users use QMD Plus to search local markdown collections through QMD with generated lexical and semantic query variants. It is especially useful when the user wants multilingual query expansion before running local QMD CLI or MCP searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search prompts may disclose query text, collection names, or other sensitive context to an external LLM provider when the optional expansion workflow is used. <br>
Mitigation: Avoid including secrets, private excerpts, API keys, confidential collection names, or other sensitive data in prompts sent to an LLM provider. <br>
Risk: LLM-generated query expansions may be inaccurate or may search for unintended concepts. <br>
Mitigation: Review the generated JSON response before executing the QMD search, especially in production or confidential knowledge bases. <br>


## Reference(s): <br>
- [QMD MCP Server Setup](references/mcp-setup.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/thehappyboy/qmd-plus) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell command snippets; helper scripts emit plain text prompts and QMD query output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QMD and, for optional query expansion, a user-selected external LLM workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
