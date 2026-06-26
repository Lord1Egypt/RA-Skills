## Description: <br>
W.A.L.V.I.S. is an AI-powered Telegram knowledge manager that saves links, text, and images, auto-tags and organizes them, stores data on Walrus decentralized storage, and exposes a web UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kuuga-0](https://clawhub.ai/user/Kuuga-0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to capture Telegram content into a searchable personal knowledge vault, sync spaces and screenshots to Walrus, and browse or manage saved items through local and hosted web interfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent OpenClaw configuration changes, add hooks and plugins, and write SOUL.md text. <br>
Mitigation: Review openclaw.json, SOUL.md, installed hooks, and installed plugins before enabling the skill in a long-running agent. <br>
Risk: The skill can upload vault data and screenshots to Walrus. <br>
Mitigation: Inspect ~/.walvis manifest, spaces, and media files before syncing, and avoid syncing sensitive content unless the storage and sharing model is acceptable. <br>
Risk: Seal and share commands can use the local Sui CLI wallet for blockchain access-control actions. <br>
Mitigation: Avoid Seal or share commands until the wallet-signing flow, target network, and access-control policy are understood. <br>
Risk: The skill may store an LLM API key locally. <br>
Mitigation: Store only scoped keys, keep local configuration private, and rotate the key if the local WALVIS configuration is exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Kuuga-0/walvis) <br>
- [WALVIS web app](https://walvis.vercel.app) <br>
- [Walrus documentation](https://docs.wal.app/) <br>
- [Walrus Sites documentation](https://docs.wal.app/walrus-sites/intro.html) <br>
- [OpenClaw documentation](https://docs.openclaw.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Telegram messages, Markdown guidance, JSON-backed configuration, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create local vault files, OpenClaw configuration entries, hooks, plugins, cron reminders, and Walrus blob references.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
