## Description: <br>
Merges a ZUGFeRD 2.1 or Factur-X invoice PDF with a time report or related PDF into a PDF/A-3b e-invoice with embedded XML for German B2B and government workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quantx-heiko](https://clawhub.ai/user/quantx-heiko) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and finance operations users can use this skill to prepare ZUGFeRD or Factur-X e-invoice PDFs that combine visible invoice and time-report pages while preserving embedded invoice XML. It is intended for German and EU electronic invoicing workflows that require PDF/A-3 and EN16931-oriented validation. <br>

### Deployment Geography for Use: <br>
Germany and European Union <br>

## Known Risks and Mitigations: <br>
Risk: The security scan verdict is suspicious and recommends human review before installation. <br>
Mitigation: Install only after reviewing the artifact and publisher, and run it in an environment appropriate for processing invoice PDFs. <br>
Risk: The workflow executes local command-line tools against invoice documents and can create or overwrite output files. <br>
Mitigation: Use explicit input and output paths, keep backups of source PDFs, and validate the generated PDF before relying on it for business or government submission. <br>
Risk: The scan guidance warns about trusting the maintainer workflow before broad use. <br>
Mitigation: Treat this as a third-party workflow, pin and review external tool downloads such as MustangProject, and require explicit approval before using it on sensitive invoices. <br>


## Reference(s): <br>
- [ZUGFeRD Standard](https://www.ferd-net.de/) <br>
- [MustangProject](https://github.com/ZUGFeRD/mustangproject) <br>
- [EN16931 Compliance](https://ec.europa.eu/digital-building-blocks/wikis/display/DIGITAL/EN16931+compliance) <br>
- [ClawHub skill page](https://clawhub.ai/quantx-heiko/zugferd-invoice) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with command-line examples and generated PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Java, GhostScript, MustangProject, and user-provided PDF inputs; generated PDFs should be validated before submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
