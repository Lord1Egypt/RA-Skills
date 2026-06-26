## Description: <br>
Deep SEO analysis and execution for on-page SEO, technical SEO, content strategy, local SEO, keyword research, and backlink risk/recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bedouijesser](https://clawhub.ai/user/bedouijesser) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
SEO practitioners, site owners, marketers, and developers use this skill to audit public web pages, rewrite SEO metadata, diagnose crawl and indexing issues, plan content and keyword opportunities, and review local SEO or backlink risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional audit script fetches public web pages supplied by the user. <br>
Mitigation: Use it only for sites the user is authorized to audit and keep routine audits limited to public HTTP or HTTPS URLs. <br>
Risk: Auditing localhost, private IP ranges, intranet hosts, or cloud metadata endpoints could expose internal systems. <br>
Mitigation: Keep the built-in refusal behavior for those targets unless the user explicitly intends internal testing in a trusted environment. <br>
Risk: The script may require Python packages that are not already installed. <br>
Mitigation: Ask before installing dependencies; when installation is not approved, fall back to manual inspection with web_fetch or browser tools. <br>


## Reference(s): <br>
- [On-Page SEO Reference](references/on-page.md) <br>
- [Technical SEO Reference](references/technical.md) <br>
- [Content Strategy & Keyword Reference](references/content-strategy.md) <br>
- [Local SEO Reference](references/local-seo.md) <br>
- [Link Building Reference](references/link-building.md) <br>
- [Platform Playbooks](references/platform-playbooks.md) <br>
- [Canada Local Notes](references/canada-local.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with optional JSON audit output and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The optional page-audit script emits structured JSON for a single public URL; narrative reports prioritize blockers, high-impact improvements, medium improvements, and next steps.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
