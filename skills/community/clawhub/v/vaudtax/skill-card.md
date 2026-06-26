## Description: <br>
Helps agents read, summarize, convert, and inspect .vaudtax files for Swiss canton Vaud tax declarations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fredj](https://clawhub.ai/user/fredj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and tax professionals use this skill to analyze Swiss canton Vaud tax declaration files, produce redacted summaries, export structured JSON, inspect deductions and supporting documents, and request Vaud tax estimates when needed. <br>

### Deployment Geography for Use: <br>
Switzerland (Canton of Vaud) <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive tax declaration data, including income, deductions, assets, and supporting documents. <br>
Mitigation: Use default redacted summaries for normal review, avoid --full unless direct identifiers are required, and do not include declaration content in web searches or external issue reports. <br>
Risk: Attachment extraction can write sensitive PDFs or images to local temporary storage. <br>
Mitigation: Extract only the attachments needed for the requested analysis and delete extracted files after review. <br>
Risk: Tax estimates may send selected fiscal inputs to the official Canton Vaud calculator. <br>
Mitigation: Run the calculator only when the user asks for an estimate and accepts sending fiscal year, commune, civil-status code, children counts, and taxable amounts to vd.ch. <br>
Risk: Tax computations and deduction checks are year- and commune-specific and can be incomplete if the declaration contains unsupported sections. <br>
Mitigation: Base numbers on script output or direct XML fields, verify the fiscal period before applying rules, disclose unsupported sections, and treat computed values as estimates unless official figures are available. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fredj/vaudtax) <br>
- [VaudTax XML namespace](http://www.vd.ch/fiscalite/vaudtax) <br>
- [Deduction rules and limits](references/deductions.md) <br>
- [Pillar attestation](references/pillar-attestation.md) <br>
- [Salary certificate](references/salary-certificate.md) <br>
- [Tax computation](references/tax-computation.md) <br>
- [XML sections](references/xml-sections.md) <br>
- [Instructions générales 2025](https://www.vd.ch/fileadmin/user_upload/organisation/dfin/aci/fichiers_pdf/21001_2025.pdf) <br>
- [ICC barème revenu 2025](https://www.vd.ch/fileadmin/user_upload/organisation/dfin/aci/fichiers_pdf/barème_revenu_2025.pdf) <br>
- [ICC barème fortune 2025](https://www.vd.ch/fileadmin/user_upload/organisation/dfin/aci/fichiers_pdf/barème_fortune_2025.pdf) <br>
- [IFD barème 2025](https://www.vd.ch/fileadmin/user_upload/organisation/dfin/aci/fichiers_pdf/Bareme_IFD_58c-2025.pdf) <br>
- [Communal tax coefficients](https://www.vd.ch/etat-droit-finances/communes/finances-communales/arretes-dimposition-et-tableaux-des-impots-communaux) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, code, guidance] <br>
**Output Format:** [Markdown summaries and code or shell snippets; JSON files conforming to vaudtax-export.schema.json when exporting.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write extracted attachments or JSON files locally when requested; summaries redact direct identifiers by default.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
