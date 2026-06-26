## Description: <br>
Audit websites for SEO, performance, security, technical, content, accessibility, and related issues using the squirrelscan CLI, returning health scores, broken links, metadata analysis, and actionable recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nc9](https://clawhub.ai/user/nc9) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, site owners, and SEO or web operations teams use this skill to audit owned or authorized websites, review prioritized findings, apply approved local code or content fixes, and compare site health before and after remediation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live website scans can affect production systems or third-party sites if run without authorization or with excessive scope. <br>
Mitigation: Use the skill only on sites you own or are authorized to test, start with limited coverage when appropriate, and be cautious with full live scans on production systems. <br>
Risk: The skill can help edit local website code or content, which may change user-facing behavior, SEO, accessibility, or compliance posture. <br>
Mitigation: Review the audit report first, approve each fix batch explicitly, keep changes on a branch when possible, and run existing build or validation checks after changes. <br>
Risk: Force-initializing squirrelscan configuration can overwrite existing local settings. <br>
Mitigation: Avoid `squirrel init --force` unless you intend to replace the current configuration. <br>


## Reference(s): <br>
- [Squirrelscan Website](https://squirrelscan.com) <br>
- [Squirrelscan Documentation](https://docs.squirrelscan.com) <br>
- [Squirrelscan Download](https://squirrelscan.com/download) <br>
- [LLM Format Output Reference](references/OUTPUT-FORMAT.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and LLM-optimized audit reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include health scores, issue lists, affected URLs, fix recommendations, regression comparisons, and proposed local code or content changes.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter lists 1.22) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
