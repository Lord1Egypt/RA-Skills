## Description: <br>
Provides a WhatsApp message formatting guide covering core syntax rules, unsupported patterns, quick-reference tables, and common message templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to look up WhatsApp-specific text formatting rules, detect unsupported Markdown-style patterns, and draft messages that use WhatsApp-compatible syntax. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests command execution for content that is primarily a static formatting guide. <br>
Mitigation: Review before installation and remove exec permission unless a maintained command-line helper is actually shipped and needed. <br>
Risk: The artifact includes nonexistent command examples and ping troubleshooting guidance. <br>
Mitigation: Remove or replace those examples so users are not guided to run irrelevant diagnostics or missing scripts. <br>
Risk: The artifact contains unrelated product-spec capability blocks that do not match the WhatsApp formatting use case. <br>
Mitigation: Delete unrelated capability text and limit the skill to WhatsApp formatting guidance, validation, and message template examples. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with text examples, bash snippets, and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Static guide content; does not require API keys or network services according to the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
