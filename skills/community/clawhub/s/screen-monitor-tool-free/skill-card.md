## Description: <br>
屏幕监控工具免费版 helps an agent trigger single or timed screen captures, save screenshots locally, and perform basic screen-content analysis for personal remote assistance, work records, and screen archives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual users, remote-support helpers, and operations users use this skill to capture current or scheduled screenshots, keep local progress records, and run basic OCR or visual analysis on captured screens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screen captures can include credentials, private messages, customer data, or other sensitive windows. <br>
Mitigation: Close or exclude sensitive windows before capture, prefer region screenshots when possible, and only run the skill when screen capture is intentional. <br>
Risk: Timed monitoring can create many saved screenshots and preserve sensitive information longer than intended. <br>
Mitigation: Use short durations, explicit output directories, and delete saved screenshots when the task is complete. <br>
Risk: Screenshot analysis may expose captured content to an LLM or external service if the surrounding agent workflow sends images or OCR text outside the local machine. <br>
Mitigation: Clarify the analysis data flow before use and avoid analyzing sensitive screenshots unless the agent environment is approved for that data. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/screen-monitor-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash command examples, structured text responses, and local PNG or JPG screenshot files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save timestamped screenshots to a user-selected local directory and may return OCR or basic analysis text when enabled.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
