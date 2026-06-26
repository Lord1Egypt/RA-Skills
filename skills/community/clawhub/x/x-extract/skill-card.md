## Description: <br>
Extracts public tweet content from x.com and twitter.com URLs without Twitter API credentials by using browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chunhualiao](https://clawhub.ai/user/chunhualiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to extract text, author details, timestamps, media links, engagement metrics, and thread context from public X/Twitter posts. It is intended for public URLs and does not support protected, private, or login-required content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens X/Twitter pages in a browser profile, which can expose account sessions or private browsing context if a logged-in profile is used. <br>
Mitigation: Use a fresh non-logged-in browser profile and avoid protected, private, age-restricted, controversial, or otherwise account-only content. <br>
Risk: Optional media downloads can save files from external source URLs. <br>
Mitigation: Approve downloads only after checking the source URL and destination path, and review downloaded files before opening or sharing them. <br>
Risk: X.com layout changes and rate limits can cause incomplete or incorrect extraction. <br>
Mitigation: Review extracted fields against the source page, use the selector reference for troubleshooting, and report clearly when required fields cannot be extracted. <br>


## Reference(s): <br>
- [X.com Content Selectors](references/selectors.md) <br>
- [X Extract README](README.md) <br>
- [ClawHub skill page](https://clawhub.ai/chunhualiao/x-extract) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Structured markdown with optional shell commands and downloaded media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write markdown instructions to a requested output file and may download media when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill.yml, CHANGELOG, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
