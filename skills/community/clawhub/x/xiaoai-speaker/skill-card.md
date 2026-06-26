## Description: <br>
小爱音箱语音播报。一句话让小爱说话，无需编写代码，支持定时提醒、远程喊话、家庭传话。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zkfan](https://clawhub.ai/user/zkfan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and household automation users use this skill to send short voice announcements to XiaoAI speakers for reminders, family messages, device testing, scheduled alerts, and remote notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide Xiaomi account credentials and contacts Xiaomi cloud services to list devices and trigger speaker announcements. <br>
Mitigation: Use only with accounts and devices you control; avoid storing MI_PASS in shell startup files or cron commands, and prefer an OS secret store, a tightly permissioned credentials file, or interactive entry. <br>
Risk: Remote or scheduled announcements can broadcast unintended or sensitive messages through household speakers. <br>
Mitigation: Restrict access to trusted users and automation, review scheduled commands before enabling them, and test with non-sensitive short messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zkfan/xiaoai-speaker) <br>
- [Skill usage guide](SKILL.md) <br>
- [README](README.md) <br>
- [MiService SDK](https://github.com/Yonsm/MiService) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text CLI output, shell command examples, and spoken speaker announcements] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Xiaomi account credentials through MI_USER and MI_PASS, with optional device selection through MI_DEVICE_NAME or MI_DEVICE_ID.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
