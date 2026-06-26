## Description: <br>
调用 Python 脚本处理文本（当前支持：转换为大写）。 / Python-powered text transformation tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[microshark2024](https://clawhub.ai/user/microshark2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to pass text to a local Python script and receive an uppercase transformed result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input text is processed by an included local Python script and displayed back to the user. <br>
Mitigation: Do not pass secrets or sensitive text unless it is intended to be transformed and shown in the response. <br>
Risk: Building raw shell commands around user text can mishandle quoted or special characters. <br>
Mitigation: Prefer clients that pass the text as a structured argument to the script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/microshark2024/text-transformer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text returned from a local Python script, with error text surfaced when execution fails.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill processes a single extracted text input and echoes the uppercase result.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
