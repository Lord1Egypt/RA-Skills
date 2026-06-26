## Description: <br>
Query OpenAI Codex OAuth account quotas in OpenClaw, switch the preferred account by email/profile id, and optionally auto-switch when 5h quota drops below a threshold. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unknown-shu](https://clawhub.ai/user/unknown-shu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect OpenClaw OpenAI Codex OAuth profile quota, switch the preferred Codex account, sync an explicit Codex CLI login, and configure quota-aware failover. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles OAuth credentials and local OpenClaw/Codex auth files. <br>
Mitigation: Install only on machines where OpenClaw should manage Codex profiles, keep auth files private, review file permissions and backups, and run dry-run commands before making changes. <br>
Risk: Imported Codex CLI credentials may be promoted to the first OpenClaw profile if the operator chooses that behavior. <br>
Mitigation: Use --no-set-first when importing credentials that should not become the preferred profile. <br>
Risk: Optional notifications can expose account status through a NapCat configuration. <br>
Mitigation: Enable notifications only with a trusted NapCat sendUrl and access token, and review logs or screenshots before sharing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/unknown-shu/unknownshu-codex-account-switcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-capable command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and openclaw; operates on local OpenClaw and Codex auth configuration.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
