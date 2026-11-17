## Description:

Merges a ZUGFeRD 2.1/Factur-X invoice PDF and a supporting time report into a PDF/A-3b e-invoice with embedded XML for German B2B and government submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quantx-heiko](https://clawhub.ai/user/quantx-heiko)

### License/Terms of Use:


## Use Case:

Developers and finance-operations users can use this skill to generate compliant German electronic invoice PDFs by combining an existing ZUGFeRD invoice with supporting time-report documentation. The primary workflow keeps both documents visible, while the fallback workflow embeds the supporting document as an attachment.

### Deployment Geography for Use:

Germany and European Union

## Known Risks and Mitigations:

Risk: The package includes temporary XML invoice artifacts containing plaintext invoice data.

Mitigation: Remove packaged temporary XML files before installation or redistribution, and avoid committing generated invoice artifacts.

Risk: The workflow relies on a persistent MustangProject JAR download whose integrity is not verified by the skill.

Mitigation: Download MustangProject from a trusted source and verify the JAR with a trusted checksum or signature before use.

Risk: Processing sensitive or untrusted invoice PDFs may expose local files or leave temporary data behind.

Mitigation: Run the workflow without elevated privileges in an isolated working directory and clean temporary files after each run.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/quantx-heiko/skills/zugferd-invoice)
- [ZUGFeRD Standard](https://www.ferd-net.de/)
- [MustangProject](https://github.com/ZUGFeRD/mustangproject)
- [EN16931 Compliance](https://ec.europa.eu/digital-building-blocks/wikis/display/DIGITAL/EN16931+compliance)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with Python workflow commands that produce PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on local Java, GhostScript, MustangProject, and input PDF validation results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
