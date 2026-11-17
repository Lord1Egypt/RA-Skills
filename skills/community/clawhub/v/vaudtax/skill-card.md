## Description:

Working with .vaudtax files (Swiss canton Vaud tax declarations).

This skill is ready for commercial/non-commercial use.

## Publisher:

[fredj](https://clawhub.ai/user/fredj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect, summarize, convert, and estimate values from Swiss Canton of Vaud .vaudtax declarations. It helps parse declaration XML, review selected supporting documents, export structured JSON, and query the official Vaud tax calculator when the user asks for a tax estimate.

### Deployment Geography for Use:

Global; designed for Swiss Canton of Vaud tax declarations.

## Known Risks and Mitigations:

Risk: The skill can expose sensitive tax declaration data and selected supporting PDFs to the agent conversation.

Mitigation: Use quick overview mode when possible, keep identifiers masked by default, and request full or attachment-level review only when it is necessary.

Risk: Attachment extraction from untrusted .vaudtax files could write files outside the intended folder.

Mitigation: Extract only selected expected attachment keys from trusted files, use a controlled temporary directory, inspect extracted paths, and delete temporary files after review.

Risk: Tax estimates can be incomplete or differ from official filed figures.

Mitigation: Treat computed values as estimates, prefer official bordereau or Gesdem figures when available, and run the official Canton Vaud calculator only when the user explicitly asks for an estimate.

Risk: Using the official calculator sends derived financial tax inputs to vd.ch.

Mitigation: Disclose that data flow before calculator use and limit the payload to the year, commune, household status counts, taxable income, and taxable wealth values.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fredj/skills/vaudtax)
- [VaudTax XML Sections](references/xml-sections.md)
- [Deduction Rules and Limits](references/deductions.md)
- [Tax Computation Guide](references/tax-computation.md)
- [Salary Certificate](references/salary-certificate.md)
- [Pillar Attestation](references/pillar-attestation.md)
- [VaudTax Export JSON Schema](vaudtax-export.schema.json)
- [Canton Vaud Instructions generales 2025](https://www.vd.ch/fileadmin/user_upload/organisation/dfin/aci/fichiers_pdf/21001_2025.pdf)
- [Canton Vaud Tax Calculator](https://www.vd.ch/etat-droit-finances/impots/impots-pour-les-individus/calculer-mes-impots)
- [Canton Vaud Communal Tax Coefficients](https://www.vd.ch/etat-droit-finances/communes/finances-communales/arretes-dimposition-et-tableaux-des-impots-communaux)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown summaries, JSON exports, command invocations, and concise guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tax estimates are derived from script output and, when requested, from the official Canton Vaud calculator.]

## Skill Version(s):

1.2.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
