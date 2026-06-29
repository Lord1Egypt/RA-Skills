## Description: <br>
Use when writing, editing, or reviewing Russian-language text, or when the user mentions ru-text; covers typography, info-style, editorial, UX writing, and business correspondence, and auto-activates on Russian text output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[talkstream](https://clawhub.ai/user/talkstream) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, UX writers, product teams, and agents use this skill to draft, rewrite, proofread, and score Russian-language text across typography, editorial style, interface copy, and business correspondence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may change typography or wording where exact character-level reproduction is required. <br>
Mitigation: Avoid or disable it for legal wording, code-adjacent strings, test fixtures, quoted material, and any task that requires exact Russian text fidelity. <br>
Risk: Editorial normalization can conflict with a user's requested register or domain-specific voice. <br>
Mitigation: Treat the user's explicit style request as higher priority than the default rules and review proposed changes before using them. <br>


## Reference(s): <br>
- [Ru Text Homepage](https://ru-text.org) <br>
- [ClawHub Skill Page](https://clawhub.ai/talkstream/skills/ru-text) <br>
- [Typography Reference](references/typography.md) <br>
- [Info-Style Reference](references/info-style.md) <br>
- [UX Writing Reference](references/ux-writing.md) <br>
- [Business Writing Reference](references/business-writing.md) <br>
- [Editorial Grammar Reference](references/editorial-grammar.md) <br>
- [Editorial Punctuation Reference](references/editorial-punctuation.md) <br>
- [Russian Text Anti-Patterns](references/anti-patterns.md) <br>
- [Text Quality Scoring](references/scoring.md) <br>
- [Sources and Attribution](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text responses with corrected Russian text, change lists, and optional 0-10 scoring diagnostics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify typography and wording; for proofreading, it should return corrected text plus a change list unless explicit in-place editing is requested.] <br>

## Skill Version(s): <br>
1.10.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
