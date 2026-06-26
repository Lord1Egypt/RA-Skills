## Description: <br>
Automates China Mobile Wangda course workflows, including course progress checks, adding new course URLs, browser-assisted login, auto-study monitoring, and stopping active study sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luobusita-ai](https://clawhub.ai/user/luobusita-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users with authorized access to China Mobile Wangda use this skill to manage course learning sessions, summarize progress, add courses, complete SMS-assisted login, and start or stop automated course monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a local browser through remote debugging and automate authenticated Wangda pages. <br>
Mitigation: Run it only in an isolated Chrome profile and only with an account approved for automation. <br>
Risk: The bundled stealth extension is injected into every site loaded by the automated Chrome profile. <br>
Mitigation: Keep the automated profile dedicated to Wangda and avoid browsing unrelated sites in that profile. <br>
Risk: The skill can receive SMS login codes and store session/account state locally. <br>
Mitigation: Use accounts and phone numbers you are comfortable automating, and clear session state when switching users. <br>
Risk: The skill can persist scheduled monitor tasks and terminate Chrome/session state. <br>
Mitigation: Review scheduled tasks after use and run the clear or stop-study workflow when automation should end. <br>
Risk: The skill can dump authenticated page contents locally. <br>
Mitigation: Store outputs only in trusted local directories and review local files before sharing logs or artifacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luobusita-ai/tmd-wangda) <br>
- [China Mobile Wangda](https://wangda.chinamobile.com) <br>
- [Tool command reference](artifact/references/tools.md) <br>
- [Session schema reference](artifact/references/schemas.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON session/progress summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local session files, control a Chrome profile, and create or remove scheduled monitor tasks.] <br>

## Skill Version(s): <br>
0.7.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
