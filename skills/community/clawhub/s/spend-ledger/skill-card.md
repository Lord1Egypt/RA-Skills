## Description: <br>
Tamper-evident payment ledger for autonomous agents — auto-detects payments across all tools, prevents duplicate payments, and presents full spending history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mattpolly](https://clawhub.ai/user/mattpolly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Spend Ledger to monitor autonomous-agent payments, review spending by service or skill, verify ledger integrity, and reduce duplicate payment attempts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill observes payment-like tool activity and writes a local spending ledger that may contain sensitive payment context. <br>
Mitigation: Install only in environments where this monitoring is acceptable, and review ledger file permissions, retention needs, and local access controls before use. <br>
Risk: Community payment-pattern syncing is enabled by default and contacts a remote service for detector updates. <br>
Mitigation: Set sync_community_patterns to false in data/config.json for sensitive, offline, or air-gapped environments. <br>
Risk: Custom tool-pattern submissions may reveal tooling patterns to maintainers. <br>
Mitigation: Avoid submitting custom patterns unless sharing those patterns is acceptable for the deployment. <br>
Risk: The security guidance identifies an argument-injection bug in query-log.sh. <br>
Mitigation: Do not pass untrusted filter strings to query-log.sh until the bug is fixed. <br>


## Reference(s): <br>
- [Spend Ledger ClawHub Listing](https://clawhub.ai/mattpolly/spend-ledger) <br>
- [Spend Ledger Homepage](https://spend-ledger.com) <br>
- [Technical Architecture](TECHNICAL.md) <br>
- [Payment Tool Signatures](references/payment-tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or text guidance with bash commands, JSON examples, dashboard URLs, and JSON spending summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local JSONL ledger records and return filtered spending views, grouped summaries, or hash-chain verification results.] <br>

## Skill Version(s): <br>
0.4.0 (source: SKILL.md frontmatter, openclaw.plugin.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
