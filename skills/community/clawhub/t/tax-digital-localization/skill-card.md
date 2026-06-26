## Description: <br>
Localizes Chinese UI and system copy for digital tax, invoice, filing, and compliance products into market-appropriate language for Vietnam, Malaysia, Singapore, Poland, Italy, and Germany. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[munich949](https://clawhub.ai/user/munich949) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product teams use this skill to translate Chinese program UI strings for tax and e-invoicing systems while preserving placeholders, keys, markup, ordering, and product-ready wording. It is intended for routine UI localization and for higher-risk tax terminology that may need authoritative or local review. <br>

### Deployment Geography for Use: <br>
Vietnam, Malaysia, Singapore, Poland, Italy, and Germany <br>

## Known Risks and Mitigations: <br>
Risk: Country-to-language defaults may not match multilingual deployments or local compliance expectations. <br>
Mitigation: Specify the exact target locale or language for each deployment, especially for Singapore, Malaysia, and other multilingual markets. <br>
Risk: Tax, invoice, filing, and compliance terms can carry legal or business meaning that a translation may not fully resolve. <br>
Mitigation: Have important tax wording reviewed by local subject-matter experts before production use, and verify high-risk terms against authoritative local sources when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/munich949/tax-digital-localization) <br>
- [UI patterns](references/ui-patterns.md) <br>
- [Tax terms](references/tax-terms.md) <br>
- [Vietnam locale](references/locales/vietnam.md) <br>
- [Malaysia locale](references/locales/malaysia.md) <br>
- [Singapore locale](references/locales/singapore.md) <br>
- [Poland locale](references/locales/poland.md) <br>
- [Italy locale](references/locales/italy.md) <br>
- [Germany locale](references/locales/germany.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Plain text translation, with an optional note line when ambiguity or semantic risk is present.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves code keys, placeholders, ICU structures, markup, field names, enum values, error codes, ordering, and line breaks when present.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
