## Description: <br>
End-to-end workflow for SEO/GEO content updates in Webflow: prioritize via GSC, draft/refresh content, create patch JSONs, update Webflow CMS via API, set images/alt/SEO, publish, and handle technical SEO fixes (canonical domain, redirects). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jchopard69](https://clawhub.ai/user/jchopard69) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External site operators, SEO practitioners, and developers use this skill to plan, draft, patch, and publish Webflow CMS content for blog, service, and local landing page SEO updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to change and publish live Webflow content with an API token. <br>
Mitigation: Use a least-privilege Webflow token, test against staging first, and require the agent to show the exact JSON diff and obtain explicit approval before any POST, PATCH, or publish action on a live site. <br>


## Reference(s): <br>
- [Webflow API v2 quick reference](references/webflow_api.md) <br>
- [SEO/GEO copy patterns](references/seo_copy_patterns.md) <br>
- [Patch templates](references/patch_templates.md) <br>
- [Webflow API v2](https://api.webflow.com/v2) <br>
- [ClawHub skill page](https://clawhub.ai/jchopard69/webflow-seo-geo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payload examples and API command patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Webflow CMS patch payloads and publishing instructions that require human review before live API changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
