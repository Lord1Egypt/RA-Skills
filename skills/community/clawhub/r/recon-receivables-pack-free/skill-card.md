## Description:

A local checker for reconciliation and receivables worksheets that runs 14 built-in checks per client directory and prints one conclusion line per client, with findings citing source file and line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance teams, general-ledger accountants, and bookkeeping receivables staff use this skill before monthly close to check reconciliation and receivables materials across client folders. It helps identify scoped ledger, aging, provision, bank reconciliation, bill, guarantee, bond, and petty-cash issues while leaving accounting judgment, audit assurance, and source-system verification to qualified reviewers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat reconciliation findings as audit assurance or accounting judgment.

Mitigation: Present outputs as reconciliation assistance only and route accounting policies, audit conclusions, assurance, and professional judgment to qualified reviewers.

Risk: Incomplete materials can leave checks unexecuted while still producing scoped output for supplied tables.

Mitigation: Review checks_not_run and sub_checks_not_run before relying on results, and provide one complete client folder with recognizable table headers for each client.

Risk: The local checker reads selected financial folders that may contain sensitive business data.

Mitigation: Run it only in trusted local environments and select only the folders intended for reconciliation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/recon-receivables-pack-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text console summary, issue details with source file and line references, or machine-readable JSON when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Node.js execution over user-selected financial folders; no network use, file writes, or persistence reported by server security evidence.]

## Skill Version(s):

1.0.31 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
