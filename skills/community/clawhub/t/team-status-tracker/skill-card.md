## Description: <br>
Systematic team status tracking via Slack DMs with confidential Obsidian-based internal tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parthpandya1729](https://clawhub.ai/user/parthpandya1729) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Managers, founders, and team leads use this skill to request project updates through Slack DMs, follow up on missing responses, and maintain internal Obsidian notes about progress, blockers, and response patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables confidential workplace monitoring of response behavior and performance-adjacent notes. <br>
Mitigation: Use it only where employee or contractor monitoring is formally approved, with clear privacy, consent, access-control, retention, and deletion rules. <br>
Risk: Slack data processing and local Obsidian storage can expose sensitive workplace information. <br>
Mitigation: Use least-privilege Slack credentials, avoid broad conversation-history collection, and restrict access to the Obsidian vault. <br>
Risk: Behavioral notes and response metrics could be used for unauthorized performance judgments. <br>
Mitigation: Do not use behavioral or performance-adjacent tracking for evaluation decisions unless formally authorized by organizational policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parthpandya1729/team-status-tracker) <br>
- [README](README.md) <br>
- [Skill guide](SKILL.md) <br>
- [Status request templates](templates/status-request.md) <br>
- [Obsidian tracking templates](templates/obsidian-tracking.md) <br>
- [Configuration template](config.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with message templates, YAML configuration, and example shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Slack and Obsidian-related skills; may use MATON_API_KEY for Slack API access.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
