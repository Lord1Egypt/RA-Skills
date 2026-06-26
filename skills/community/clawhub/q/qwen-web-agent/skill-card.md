## Description: <br>
Automates the Qwen web interface at qianwen.com with Playwright to submit prompts, maintain a browser login session, and capture single-turn or multi-turn responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dereksongyang](https://clawhub.ai/user/dereksongyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to route prompts to Qwen's web chat and bring the resulting Markdown or text answers into automated workflows that need single-turn or multi-turn Q&A. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a reusable Qwen browser login session on disk. <br>
Mitigation: Use it only on trusted machines and review or remove the saved session directory when access should no longer persist. <br>
Risk: Prompts are sent to qianwen.com and chat contents are saved in plain-text Markdown files. <br>
Mitigation: Avoid submitting secrets or private documents, and change the output paths before use in shared or sensitive environments. <br>
Risk: The scripts can automatically delete Qwen conversations from the logged-in account. <br>
Mitigation: Review the scripts before installation and disable deletion unless that behavior is explicitly wanted. <br>


## Reference(s): <br>
- [Qwen usage instructions](references/使用说明.md) <br>
- [Qwen web interface](https://www.qianwen.com/) <br>
- [ClawHub skill page](https://clawhub.ai/dereksongyang/qwen-web-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text captured from Qwen responses, with command-line status output during execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single-turn runs write the latest response to last_output.md; multi-turn runs write conversation history to qwen_session_history.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
