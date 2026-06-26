## Description: <br>
Xint is an X/Twitter intelligence CLI that helps agents search, monitor, analyze, engage with, and export X discourse from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xNyk](https://clawhub.ai/user/0xNyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use Xint to gather recent X/Twitter discourse, analyze sentiment or trends, monitor topics, follow threads, and export findings for briefings or local knowledge workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad OAuth permissions can allow account actions beyond read-only research. <br>
Mitigation: Start with read-only use, grant only required scopes, and avoid tweet.write unless the release explicitly justifies it. <br>
Risk: The package API server can expose powerful local functions if run without authentication. <br>
Mitigation: Configure bearer authentication before starting any package API server and keep network listeners disabled unless needed. <br>
Risk: Collection sync and export features can copy private files, sensitive queries, or token-related data into local outputs. <br>
Mitigation: Do not sync private directories, review exported files before sharing, and keep OAuth tokens in restricted local storage. <br>
Risk: Webhook delivery can send search or monitoring data to remote endpoints. <br>
Mitigation: Use HTTPS endpoints, configure an allowlist for trusted webhook hosts, and avoid sending sensitive queries to third-party destinations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/0xNyk/xint) <br>
- [X API reference notes](references/x-api.md) <br>
- [Skill README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Terminal text, JSON, JSONL, CSV, Markdown, and saved local files depending on command options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write cache, exports, snapshots, OAuth tokens, and Obsidian bookmark-sync files under local data paths.] <br>

## Skill Version(s): <br>
2026.2.26 (source: server release evidence; package.json reports 2026.3.16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
