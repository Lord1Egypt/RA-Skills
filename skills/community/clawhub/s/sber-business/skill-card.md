## Description:

Connects to the SberBusiness API for account balances, transaction alerts, payment drafts, statement downloads, and credential rotation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[synthet1x](https://clawhub.ai/user/synthet1x)

### License/Terms of Use:

MIT-0

## Use Case:

Business account operators use the skill to review balances and transactions, create payment drafts for signing, and download bank-stamped statements. It also guides account setup and transaction alert configuration.

### Deployment Geography for Use:

Russia

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because it handles banking credentials and decrypted private keys.

Mitigation: Review credential handling and confirm that shell and network access are appropriate for the installation.

Risk: The scan is partial because some referenced local paths did not resolve, leaving evidence incomplete.

Mitigation: Review the complete referenced files and runtime paths before relying on the scan assessment.

Risk: Secrets sent in requests could be exposed through URL logging.

Mitigation: Check request and proxy logging so secrets are not recorded in URLs.

## Reference(s):

- [SberBusiness portal](https://sbi.sberbank.ru)
- [HUMAN_GUIDE.md](references/HUMAN_GUIDE.md)
- [NOTIFICATION_CHANNELS.md](references/NOTIFICATION_CHANNELS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance, shell commands, banking API result text, signing links, and PDF statements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return account and transaction information, payment signing links, and bank-stamped PDF statements.]

## Skill Version(s):

1.2.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
