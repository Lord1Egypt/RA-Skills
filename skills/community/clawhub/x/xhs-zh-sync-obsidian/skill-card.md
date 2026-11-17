## Description:

Synchronizes Xiaohongshu and Zhihu favorites into Obsidian by guiding setup, CookieCloud authentication, hctec scraper dependencies, classification rules, Markdown export, and optional OpenClaw cron generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunfang1cn](https://clawhub.ai/user/sunfang1cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install, configure, diagnose, and automate a workflow that archives social-platform favorites into an Obsidian vault.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser cookies and CookieCloud credentials can expose Xiaohongshu or Zhihu sessions if copied into chat, logs, or shared artifacts.

Mitigation: Keep cookiecloud.env, raw cookies, logs, state files, downloaded notes, images, and vault exports local; avoid pasting Obsidian or encryption passwords into chat and rotate any credentials exposed in logs.

Risk: A remotely exposed CookieCloud service can make browser login state reachable outside the intended machine or network.

Mitigation: Use a dedicated local CookieCloud instance when possible, bind it to localhost or a protected network, and restrict permissions on cookiecloud.env.

Risk: The sync workflow installs and runs third-party hctec scraper skills and Python/Node dependencies.

Mitigation: Review and pin dependency versions and inspect downloaded third-party skills before running sync or cron automation.

Risk: Automated cron sync can repeatedly access logged-in social accounts and write personal content into an Obsidian vault.

Mitigation: Start with small manual syncs, confirm exported content and vault location, then enable scheduled jobs only with expected platforms, times, and notification behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sunfang1cn/skills/xhs-zh-sync-obsidian)
- [First Install](references/first-install.md)
- [CookieCloud Authentication](references/auth.md)
- [Configuration](references/config.md)
- [Dependencies](references/dependencies.md)
- [Obsidian Sync](references/obsidian-sync.md)
- [Cron](references/cron.md)
- [Obsidian Layout](references/obsidian-layout.md)
- [CookieCloud](https://github.com/easychen/CookieCloud)
- [hctec Collection Skills](https://github.com/hc-tec/my-collection-skills/tree/main/skills)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON]

**Output Format:** [Markdown guidance with inline shell commands; scripts produce JSON status and Obsidian Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local runtime configuration, CookieCloud environment files, raw JSON state, downloaded media, and Obsidian vault content on the user's machine.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
