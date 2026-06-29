## Description: <br>
Renders structured cross-border ecommerce data into deterministic PNG information graphics such as size charts, specification cards, feature grids, comparison tables, and promotional banners through Yufluent's server-side Pillow service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metahuan](https://clawhub.ai/user/metahuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce sellers, operators, and agent developers use this skill to turn product facts and template data into rendered commerce assets for marketplace listings and promotional content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud rendering sends product data and TOKENAPI_KEY-authenticated requests to the configured service. <br>
Mitigation: Install only when you trust Yufluent with the rendered product data, keep TOKENAPI_KEY secret, and rotate the key if exposure is suspected. <br>
Risk: TOKENAPI_BASE_URL can redirect requests to a custom endpoint, and fallback agent routing exists when the normal render endpoint fails. <br>
Mitigation: Set TOKENAPI_BASE_URL only to a trusted endpoint and review endpoint configuration before using the skill in production workflows. <br>
Risk: Rendered ecommerce assets may misrepresent products if supplied specifications, claims, or comparison data are inaccurate. <br>
Mitigation: Review input data and rendered images against authoritative product documentation before publishing commerce assets. <br>
Risk: Fonts used for Chinese or multilingual rendering may have separate licensing requirements. <br>
Mitigation: Use appropriately licensed fonts, such as organization-approved system fonts or reviewed Noto Sans SC deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metahuan/yufluentcn-ecommerce-render) <br>
- [Yufluent console](https://claw.changzhiai.com) <br>
- [OpenClaw integration](https://claw.changzhiai.com/app/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Files] <br>
**Output Format:** [CLI text or JSON response referencing server-rendered PNG output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOKENAPI_KEY; template output is rendered server-side and may be billed per image.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
