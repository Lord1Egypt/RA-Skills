## Description: <br>
Run long-horizon, multi-step browser automation by delegating to the Microsoft webwright CLI, which writes and executes Playwright scripts to drive a real Chromium browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hansraj316](https://clawhub.ai/user/hansraj316) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Webwright to delegate authorized multi-step browser workflows, including logins, forms, checkout or wizard flows, and repeatable site navigation, to a real browser automation CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can take real actions on live sites and spend model-provider tokens. <br>
Mitigation: Use the skill only for user-authorized sites and tasks, keep the task and start URL scoped, avoid destructive actions, and review outputs before reuse. <br>
Risk: Secret values in task text, configuration, logs, or run artifacts can be exposed to the model provider or stored locally. <br>
Mitigation: Pass credentials through environment variable names or an intentionally chosen browser profile, and never put literal passwords or tokens in the task text. <br>
Risk: A mismatched local Python, Playwright, or Chromium setup can cause generated browser scripts to fail or write outputs in the wrong place. <br>
Mitigation: Use an isolated CLI install, run setup checks before use, and keep the output directory inside the current workspace. <br>


## Reference(s): <br>
- [ClawHub Webwright skill page](https://clawhub.ai/hansraj316/webwright) <br>
- [Webwright upstream project](https://github.com/microsoft/webwright) <br>
- [CLI reference](artifact/references/cli.md) <br>
- [Setup guide](artifact/references/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated Python/Playwright scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Run artifacts may include generated scripts, plans, logs, and screenshots in the selected workspace output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
