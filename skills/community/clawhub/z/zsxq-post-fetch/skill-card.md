## Description: <br>
Fetches, searches, summarizes, and exports Knowledge Planet posts that the user's authenticated account is authorized to access, using the official zsxq-cli path by default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wufulin](https://clawhub.ai/user/wufulin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve, inspect, summarize, search, and export Knowledge Planet content available to their own authenticated accounts. It supports configured groups, date ranges, digest filtering, Markdown export, and optional attachment handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and export private Knowledge Planet account content. <br>
Mitigation: Use explicit group IDs, date ranges, counts, and scopes; treat generated Markdown and attachments as private data. <br>
Risk: Legacy HTTP fallback requires the sensitive ZSXQ_TOKEN credential. <br>
Mitigation: Prefer the official zsxq-cli login path, leave ZSXQ_BACKEND unset, and set ZSXQ_TOKEN only when legacy fallback is specifically required. <br>
Risk: Automatic attachment downloads may save private files locally. <br>
Mitigation: Disable download_attachments in config.json when downloads are not needed and review local output paths before sharing files. <br>


## Reference(s): <br>
- [Architecture](docs/architecture.md) <br>
- [API Reference](references/api-reference.md) <br>
- [Official zsxq-cli](https://github.com/unnoo/zsxq-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Chinese natural-language responses, JSON command output, Markdown exports, local attachment files, and shell/configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write Markdown and downloaded attachments under the configured attachment directory; exported content should be treated as private account data.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
