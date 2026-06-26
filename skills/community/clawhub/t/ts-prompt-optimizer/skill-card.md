## Description: <br>
Optimizes prompt-style user requests into clearer, more specific task descriptions using prefix triggers, configurable model routing, and personalized rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chen435636097](https://clawhub.ai/user/chen435636097) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn short or ambiguous prompts into structured task instructions for coding, writing, analysis, and creative workflows. It is designed for OpenClaw-style agents and uses optional API keys for DeepSeek and Bailian/Qwen model providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt history may be retained locally, including sensitive prompt content. <br>
Mitigation: Avoid confidential prompts unless history retention is disabled or cleaned regularly, and review local OpenClaw files after use. <br>
Risk: API keys may be stored or exposed through local configuration flows. <br>
Mitigation: Keep credentials in environment variables or an operating-system secret store, and avoid displaying configuration with real keys present. <br>
Risk: Generated optimized prompts may add assumptions or constraints the user did not intend. <br>
Mitigation: Review optimized prompts before execution, especially for code, security, legal, financial, or operational tasks. <br>


## Reference(s): <br>
- [ClawHub listing for ts-prompt-optimizer](https://clawhub.ai/chen435636097/ts-prompt-optimizer) <br>
- [Publisher profile: chen435636097](https://clawhub.ai/user/chen435636097) <br>
- [OpenClaw ClawHub homepage](https://github.com/openclaw/clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with optional inline code blocks and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local configuration and prompt-history files when its setup and optimization scripts are used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter and release notes list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
