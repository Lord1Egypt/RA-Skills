## Description: <br>
SEO-Awesome guides agents through first-party Google API driven SEO workflows for keyword research, pSEO page generation, staged publishing, monetization, and GA4-based review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adsorgcn](https://clawhub.ai/user/adsorgcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Site owners, marketers, and builders use this skill to plan and operate automated SEO workflows that use Google APIs, LLM-assisted content assembly, staging review, publishing controls, and GA4 feedback. It is intended for websites and accounts they control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google and GA4 credentials could be exposed or over-permissioned during automation setup. <br>
Mitigation: Store credentials only in secrets or environment variables and grant readonly analytics permissions where possible. <br>
Risk: Automated SEO publishing could make large or incorrect production changes. <br>
Mitigation: Review generated pages in staging, require human approval for production publishing, and keep rollback available. <br>
Risk: GA4-derived decisions may process sensitive business or visitor behavior data. <br>
Mitigation: Use the skill only on sites and accounts you control and retain only the aggregate analytics needed for review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adsorgcn/seo-awesome) <br>
- [iLang homepage](https://ilang.ai) <br>
- [Gefei SEO](https://seo.web.cafe/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with commands, configuration snippets, workflow steps, and review checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only skill; does not execute API calls or publish content by itself.] <br>

## Skill Version(s): <br>
1.2.5 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
