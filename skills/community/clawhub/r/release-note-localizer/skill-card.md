## Description: <br>
Release Note Localizer converts release notes into Chinese, English, customer-facing, and technical versions while keeping terminology consistent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Documentation, localization, release, and customer-communication teams use this skill to turn raw release notes and terminology requirements into reviewable multilingual Markdown drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Localized release notes may be inappropriate for sensitive legal contracts or professional legal translation. <br>
Mitigation: Use the skill for product and technical release-note content, and route legal or contractual material to qualified legal and translation review. <br>
Risk: Inputs may contain confidential roadmap details, customer data, or other sensitive release material. <br>
Mitigation: Review and sanitize input before use, and prefer dry-run/stdout or a deliberate output path for generated files. <br>
Risk: Incomplete source notes can lead to uncertain terminology or misleading localized wording. <br>
Mitigation: Keep the generated terms-to-confirm section in the review workflow and require human approval before publication. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/52YuanChangXing/release-note-localizer) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown by default, with optional JSON from the local helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured sections include glossary, Chinese version, English version, customer version, technical version, and terms to confirm.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
