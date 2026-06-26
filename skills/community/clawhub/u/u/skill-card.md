## Description: <br>
Universal Utility Toolkit - 全能实用工具包 provides common developer utilities for unit conversion, UUID generation, URL handling, Unicode exploration, JSON/YAML formatting, hash calculation, password generation, and color conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgta23](https://clawhub.ai/user/hgta23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for everyday utility tasks such as converting units, generating UUIDs or passwords, encoding and decoding URLs or Base64 text, formatting structured data, calculating hashes, and converting color values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Currency conversion output may be inaccurate because the security guidance notes that rates are hardcoded. <br>
Mitigation: Treat currency conversions as approximate and verify current rates with a trusted financial data source before making decisions. <br>
Risk: The artifact README includes an npm install example, and the security guidance recommends verifying any separately installed package name. <br>
Mitigation: Confirm the package identity and publisher before running installation commands. <br>
Risk: The toolkit includes password generation and strength scoring, but generated credentials still depend on user-selected options. <br>
Mitigation: Use strong length and character settings, review generated values before use, and follow the consuming system's credential policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hgta23/u) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks, plain text utility results, and structured values where useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include converted values, UUIDs, passwords, hashes, encoded strings, formatted JSON/YAML/Base64, and color values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
