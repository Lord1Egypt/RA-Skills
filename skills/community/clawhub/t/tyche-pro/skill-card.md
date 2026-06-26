## Description: <br>
Tyche Pro — Invoice & Fortune Engine generates professional PDF-ready invoices, tracks multi-currency payments, applies tax and late fee calculations, sends tiered reminder emails, and exports a full revenue analytics dashboard from a CSV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Freelancers, small businesses, and billing operators use this skill to generate invoice reports, track outstanding payments, calculate taxes and late fees, and review receivables analytics from a local CSV workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles financial invoice and payment data and writes local report files. <br>
Mitigation: Run it from a private working directory and keep generated Markdown and CSV reports out of shared, synced, or source-controlled folders unless that sharing is intentional. <br>
Risk: The skill requires an external license purchase flow and a LICENSE_KEY value. <br>
Mitigation: Install only when the publisher and purchase flow are trusted, and store the license key in an environment variable rather than in source files or shared documentation. <br>
Risk: The setup installs the PyPI rich dependency before running the workflow. <br>
Mitigation: Use a trusted Python environment and review dependency installation policy before running the install command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/tyche-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands, Python code, console tables, generated Markdown report, and generated CSV analytics file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a LICENSE_KEY environment variable and may read invoice data from INVOICES_FILE; generated report and analytics files are written locally.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
