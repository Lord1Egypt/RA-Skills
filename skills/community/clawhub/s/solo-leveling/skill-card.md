## Description: <br>
Solo Leveling is a life RPG skill that turns real-world habits into an agent-managed progression system with stats, ranks, daily quests, dungeons, titles, and proof-based accountability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolmoses](https://clawhub.ai/user/anmolmoses) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to have an agent configure and run a gamified habit tracker for fitness, learning, sleep, creative work, and other recurring goals. The agent issues quests, asks for proof, records XP and stat changes, generates status reports, and can propose scheduled reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes bundled personal configuration and player history. <br>
Mitigation: Remove the bundled Annu config and player or quest history before using the skill for a new user. <br>
Risk: The skill can set up recurring cron-based reminders and accountability checks. <br>
Mitigation: Review the exact cron entries, timezone conversions, and removal steps before allowing scheduled jobs. <br>
Risk: Optional Twilio and ElevenLabs integrations can place phone calls using user-provided credentials. <br>
Mitigation: Add credentials only when phone-call reminders are desired, and store those credentials outside shared workspaces. <br>
Risk: The ElevenLabs call path can upload generated reminder audio to transfer.sh for Twilio playback. <br>
Mitigation: Disable that upload path or replace it with private storage before sending sensitive reminder content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/anmolmoses/solo-leveling) <br>
- [Publisher profile](https://clawhub.ai/user/anmolmoses) <br>
- [Game mechanics reference](references/game-mechanics.md) <br>
- [Configuration template](references/config-template.json) <br>
- [Preset configurations](references/presets/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown-style agent messages, JSON configuration and state files, Python CLI output, shell commands, and optional Twilio or ElevenLabs API call results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local player and quest-log JSON state; optional phone-call reminders require user-provided Twilio and ElevenLabs credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
