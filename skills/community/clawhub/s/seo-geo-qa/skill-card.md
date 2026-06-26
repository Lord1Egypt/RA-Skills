## Description: <br>
Checks blog posts and articles before or after publishing for broken links, weak sources, missing SEO elements, citation problems, and publish-readiness verdicts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justinbao19](https://clawhub.ai/user/justinbao19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content teams, editors, marketers, and developers use this skill to audit draft or published articles, generate Markdown and JSON QA reports, and identify issues to fix before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts external sites and Jina Reader during normal SEO, link, and SERP checks. <br>
Mitigation: Install only when external network checks are acceptable; avoid embargoed drafts, internal or staging links, and sensitive URLs unless that exposure is approved, and use --skip-serp or --no-jina when appropriate. <br>


## Reference(s): <br>
- [Configuration](references/configuration.md) <br>
- [Source Tiers](references/source-tiers.md) <br>
- [Verdict Rules](references/verdict-rules.md) <br>
- [Example QA Report](references/example-report.md) <br>
- [Jina Reader](https://r.jina.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON reports with command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include PASS, FAIL, or REVISE verdicts, link status, source tiering, SEO checks, SERP gap analysis, warnings, and next actions.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
