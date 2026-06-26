## Description: <br>
Compile markdown documents with plugin tags into editorial-quality HTML pages using Wurd. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vreff](https://clawhub.ai/user/vreff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content authors use this skill to create Wurd documents, configure layout and theme frontmatter, add built-in plugin tags, and debug compilation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LLM-powered plugins may send document or prompt content to the configured LLM provider and cache responses locally. <br>
Mitigation: Use an approved provider for sensitive work, avoid sensitive or proprietary documents when approval is unclear, and use --no-cache or clear .cache/llm/ when cached outputs should not persist. <br>
Risk: External plugin loading can execute behavior from local plugin directories. <br>
Mitigation: Load plugins only from trusted directories and review custom plugin code before using it in production document builds. <br>


## Reference(s): <br>
- [Wurd project](https://github.com/vreff/Wurd) <br>
- [ClawHub Wurd skill page](https://clawhub.ai/vreff/wurd) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agent responses for Wurd document compilation, plugin use, LLM setup, and troubleshooting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
