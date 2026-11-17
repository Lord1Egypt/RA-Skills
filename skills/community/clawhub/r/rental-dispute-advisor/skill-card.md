## Description:

处理中国租房押金不退、房东扣押金、提前退租、中介费、维修责任、涨租和退租争议；输出事实清单、证据包、赔偿估算、催告函、12315/住建委投诉路径和协商话术。

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users, especially tenants in China, use this skill to structure rental deposit and lease disputes, assess evidence gaps, estimate recoverable amounts, draft demand or complaint text, and plan escalation through negotiation, mediation, 12315, housing authorities, arbitration, or court where appropriate.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The local script has unsafe input-file handling that could allow a crafted filename to run code on the user's machine.

Mitigation: Review before installing, and do not run the script on JSON files or paths from untrusted sources until the Python path handling is fixed.

Risk: Generated letters, legal analysis, dates, and escalation recommendations may be incomplete or outdated for a specific city or dispute.

Mitigation: Treat outputs as drafts, verify current local law and deadlines, and consult a licensed lawyer or local housing authority for important matters.

Risk: Rental dispute case files can contain sensitive personal, financial, housing, and conflict details.

Mitigation: Avoid storing case files in shared or synced folders unless that exposure is intended.

## Reference(s):

- [Deposit Dispute Playbook](references/deposit-dispute-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-style structured reports, with shell command examples for the bundled CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include legal-information disclaimers, evidence checklists, amount estimates in RMB, demand letters, complaint packages, negotiation scripts, and escalation timelines.]

## Skill Version(s):

1.1.0 (source: release evidence, SKILL.md frontmatter, skill.json, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
