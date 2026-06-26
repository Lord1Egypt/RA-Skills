## Description: <br>
AI搜索引擎诊断助手 reviews SEO/AEO article drafts, URLs, or files and returns summaries, diagnostic conclusions, prioritized recommendations, and reusable deliverables for search and AI citation readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allinherog-star](https://clawhub.ai/user/allinherog-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, operations teams, marketers, and technical teams use this skill to evaluate whether article content is ready for SEO/AEO discovery and AI citation. It helps turn goals, audiences, article text, files, or public URLs into concise diagnostics, priorities, and next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Article drafts, files, URLs, API credentials, tenant metadata, and profile context may be sent to ai-skills.ai or the configured AISKILLS_BASE_URL. <br>
Mitigation: Use only content appropriate for that external service, avoid confidential or regulated material, and confirm privacy, retention, and access controls before sensitive use. <br>
Risk: The runner requires an API key and tenant configuration. <br>
Mitigation: Store credentials in environment variables, avoid placing secrets in prompts or parameter JSON, and rotate keys if they are exposed. <br>
Risk: The OpenAI agent config allows implicit invocation while the runner can call an external endpoint. <br>
Mitigation: Prefer explicit invocation for this skill and review the target base URL and request parameters before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/allinherog-star/seo-article-review) <br>
- [Form schema](references/form-schema.json) <br>
- [Skill metadata](references/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON envelope containing human-readable SEO/AEO analysis and reusable artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISKILLS_API_KEY; accepts article text, uploaded article files, public article URLs, goals, audience context, keywords, target platform, review depth, and brand constraints.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
