## Description: <br>
Scans WeChat public-account articles for sensitive compliance terms, produces a violation report, and can rewrite flagged wording into safer alternatives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarezoe](https://clawhub.ai/user/clarezoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and developers preparing Chinese-language WeChat public-account articles use this skill to find sensitive terms, review severity and line-numbered findings, and optionally produce safer replacement wording before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic rewrite mode can change article wording and may alter nuance or over-apply conservative replacements. <br>
Mitigation: Use report-only mode for review drafts, inspect all suggestions and [REVIEW] markers, and rely on the generated backup before accepting file changes. <br>
Risk: Sensitive-word lists and platform enforcement rules can become outdated or miss context-dependent issues. <br>
Mitigation: Treat the report as a pre-publication aid, keep the sensitive-words reference current, and perform human compliance review before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clarezoe/wechat-compliance-check) <br>
- [Project homepage](https://github.com/nicekate/wechat-compliance-check) <br>
- [Sensitive words reference](references/sensitive-words.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, files] <br>
**Output Format:** [Markdown report with line-numbered findings, rewrite suggestions, and optional modified article files with backups.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report-only mode leaves source files unchanged; fix mode backs up the original file and marks context-dependent terms for human review.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
