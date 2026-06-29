## Description: <br>
Audit and optimize websites for technical SEO, GEO / AI visibility, and Core Web Vitals using local build-output checks, live URL checks, and focused remediation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cosmofang](https://clawhub.ai/user/cosmofang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and launch reviewers use this skill to audit rendered website output and deployed origins for SEO, AI crawler visibility, structured data, canonical metadata, page-weight gates, and LCP / Core Web Vitals issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the live audit against a site without authorization can create unwanted external requests. <br>
Mitigation: Run live checks only against sites the user is authorized to test. <br>
Risk: SEO, robots.txt, llms.txt, canonical URL, and crawler-access recommendations can affect search and AI crawler visibility. <br>
Mitigation: Review proposed source changes before applying them and re-run the audits after changes. <br>
Risk: Auditing the wrong local directory can produce misleading SEO findings because the local auditor expects rendered build output. <br>
Mitigation: Point the local audit at the intended build-output directory, not source templates. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cosmofang/seo-geo-gate) <br>
- [Publisher Profile](https://clawhub.ai/user/cosmofang) <br>
- [Homepage](https://github.com/Cosmofang/seo-audit) <br>
- [Hard Gates](references/hard-gates.md) <br>
- [Structured Data Recipes](references/structured-data.md) <br>
- [GEO AI Visibility](references/geo-ai-visibility.md) <br>
- [LCP Playbook](references/lcp-playbook.md) <br>
- [Build-Time SEO Gates Case Study](analysis/case-study-build-time-seo-gates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON audit output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled audit scripts print reports to stdout; output is persisted only when redirected by the user.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
