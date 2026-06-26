## Description: <br>
Universal Agent automates end-to-end tasks by interpreting natural language, generating shell commands or Python scripts, executing them, retrying on errors, and summarizing results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to delegate natural-language tasks that require generating and running shell commands or Python scripts, such as file operations, data processing, CLI workflows, API calls, and task-result summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a broad autonomous command-and-script executor and can affect files, accounts, external services, or connected systems. <br>
Mitigation: Run it only in a disposable, low-privilege sandbox and inspect generated commands or scripts before execution. <br>
Risk: Persistent memory and task context may retain sensitive information from prior work. <br>
Mitigation: Disable memory or use a temporary memory file for sensitive work, and avoid placing secrets or production data in task prompts. <br>
Risk: Dangerous mode can bypass confirmation for high-risk actions. <br>
Mitigation: Keep dangerous mode disabled and avoid hardware control, account actions, financial or business mutations, and broad filesystem tasks without stronger containment and confirmation controls. <br>


## Reference(s): <br>
- [Universal Agent README](references/README.md) <br>
- [ClawHub Universal Agent release page](https://clawhub.ai/wangjiaocheng/universal-agent) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/wangjiaocheng) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Natural-language summaries, generated command/script content, and structured JSON results in bridge mode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute generated commands or Python scripts, write temporary files, persist memory, and call configured LLM-compatible APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
