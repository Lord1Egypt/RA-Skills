## Description: <br>
Syncs Xiaohongshu and Zhihu favorites into an Obsidian vault using CookieCloud session state, hctec scraping skills, classification rules, Markdown export, and optional OpenClaw cron setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunfang1cn](https://clawhub.ai/user/sunfang1cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and individual users use this skill to install, configure, diagnose, archive, classify, export, and schedule syncing of social-platform favorites into Obsidian. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles browser session cookies and Obsidian credentials. <br>
Mitigation: Keep CookieCloud credentials, raw cookies, Obsidian passwords, encryption keys, logs, and exported content private on the user's machine; prefer interactive Obsidian login and do not paste secrets into chat. <br>
Risk: The skill installs and patches unpinned third-party scraping dependencies. <br>
Mitigation: Install only if the publisher, hctec scraping skills, CookieCloud, and obsidian-headless are trusted; review or pin the external hctec dependency before scheduled use. <br>
Risk: Generated cron jobs can repeatedly run sync and export workflows. <br>
Mitigation: Review generated cron payloads before enabling them and start with manual sync checks before scheduled operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunfang1cn/xhs-zh-sync-obsidian) <br>
- [First install guide](references/first-install.md) <br>
- [CookieCloud authentication guide](references/auth.md) <br>
- [Dependency guide](references/dependencies.md) <br>
- [Obsidian sync guide](references/obsidian-sync.md) <br>
- [Cron guide](references/cron.md) <br>
- [CookieCloud](https://github.com/easychen/CookieCloud) <br>
- [hctec collection skills dependency](https://github.com/hc-tec/my-collection-skills/tree/main/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code] <br>
**Output Format:** [Markdown guidance with bash commands and generated JSON/YAML configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local configuration files, Obsidian Markdown exports, media assets, and OpenClaw cron payloads when the user runs the recommended commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
