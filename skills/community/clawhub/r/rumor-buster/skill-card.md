## Description: <br>
Rumor Buster verifies news, claims, and messages with Chinese and English cross-verification, source tracing, and credibility scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harry720320](https://clawhub.ai/user/harry720320) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check whether a claim, message, or news item is credible by searching Chinese and English sources, comparing findings, tracing origins, and producing a concise verification report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Verification text may be sent to external search providers. <br>
Mitigation: Do not submit private messages, credentials, confidential documents, or regulated data unless external lookup exposure is acceptable. <br>
Risk: The Tavily integration includes insecure API-key handling, including a hardcoded fallback key and plaintext local configuration. <br>
Mitigation: Remove the hardcoded fallback key before use, provide Tavily credentials through a managed secret or environment variable, and avoid storing personal API keys in plaintext config. <br>
Risk: Implicit or ambiguous invocation could cause unintended external verification requests. <br>
Mitigation: Use explicit /verify and /rumor-buster setup commands so users clearly choose when verification and setup actions run. <br>


## Reference(s): <br>
- [Verification Workflow Guide](references/verification-guide.md) <br>
- [Architecture & Sub-Skill Integration](references/architecture.md) <br>
- [Output Templates](references/output-templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/harry720320/rumor-buster) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown verification summaries and detailed reports, with setup guidance and optional shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese or English output may include credibility scores, source timelines, cross-verification tables, and search result links.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
