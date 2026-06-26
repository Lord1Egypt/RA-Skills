## Description: <br>
Automatically segments OKKI CRM customers into five tiers, scores lifecycle and value signals, syncs tags, and generates strategy recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CRM operators use this skill to collect OKKI CRM customer data, score accounts into VIP, active, normal, dormant, and lost segments, generate recommended follow-up strategies, and optionally sync segment tags back to OKKI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses an OKKI CRM account and local OKKI config or token files. <br>
Mitigation: Use least-privileged OKKI credentials and review or override OKKI_WORKSPACE and ENV_PATH before running it. <br>
Risk: Raw customer data, generated recommendations, logs, and backups may contain sensitive customer information. <br>
Mitigation: Treat generated data and logs directories as sensitive; do not commit, broadly back up, or share them. <br>
Risk: Tag synchronization can write customer segment tags back to OKKI CRM. <br>
Mitigation: Use dry-run mode and small --limit batches before running with --confirm. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cjboy007/ssa-customer-segmentation) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, JSON data files, and text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes customer data, scores, strategy recommendations, metrics, logs, and tag backups to local data and logs directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
