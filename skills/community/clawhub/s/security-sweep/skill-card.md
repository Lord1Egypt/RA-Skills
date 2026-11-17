## Description:

Security scanner for OpenClaw skills and plugins. Scans for hardcoded secrets, dangerous exec patterns, dependency vulnerabilities, and network egress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rhombusmaximus](https://clawhub.ai/user/rhombusmaximus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to audit OpenClaw skills and plugins before installation, publishing, or security review. It helps identify hardcoded secrets, unsafe execution patterns, dependency vulnerabilities, shell injection surfaces, and unexpected network egress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional --encrypt-found path can pass discovered secrets through a local Notion helper and external storage.

Mitigation: Use normal scan/report mode by default. Enable --encrypt-found only after reviewing the local Notion helper, setting NOTION_MASTER_PASSWORD securely, and confirming the Notion storage model is acceptable.

Risk: Scan reports may contain sensitive paths or source lines related to credentials.

Mitigation: Treat generated reports as sensitive, review findings before sharing, and rotate any credential confirmed to have been exposed.

## Reference(s):

- [Notion Encryption System](artifact/references/notion-encryption.md)
- [Notion API integrations](https://www.notion.so/my-integrations)
- [ClawHub security-sweep listing](https://clawhub.ai/rhombusmaximus/skills/security-sweep)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and plain-text scan reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include finding categories, affected paths, severity counts, and recommended actions.]

## Skill Version(s):

1.1.2 (source: server release evidence; artifact frontmatter says 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
