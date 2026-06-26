## Description: <br>
Intelligent product management for AI service providers on Xianyu platform with professional templates, dry-run review, and enforced confirmation for product creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crab-xieyujin](https://clawhub.ai/user/crab-xieyujin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and developers use this skill to prepare, preview, and publish Xianyu marketplace listings for AI services, including templated product descriptions, pricing tiers, batch variants, and poster prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prepare and publish Xianyu marketplace listings, including batch listing creation, and the server security summary reports that some paths do not enforce an approval step in this artifact. <br>
Mitigation: Use dry_run first, review all listing content and claims before publishing, and avoid the _unsafe methods unless a separate approval process is in place. <br>
Risk: Unsafe publish methods can bypass confirmation and may create marketplace listings with privileged credentials. <br>
Mitigation: Use dedicated low-permission credentials, supply user_name explicitly, and review the separate xianyu-api-client-skill security model before deployment. <br>
Risk: Generated listings may contain inaccurate service claims, pricing, or customer outcome statements. <br>
Mitigation: Verify titles, descriptions, prices, images, and performance claims against the actual service offering before any publish call. <br>


## Reference(s): <br>
- [Goofish / Xianyu Open Platform](https://www.goofish.pro) <br>
- [ClawHub source listing](https://clawhub.com/skills/xianyu-product-manager) <br>
- [ClawHub skill page](https://clawhub.ai/crab-xieyujin/xianyu-product-manager-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance, API calls] <br>
**Output Format:** [Markdown/text guidance with Python data structures and JSON-like product payload previews] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can prepare Xianyu listing data, poster prompts, dry-run previews, and marketplace publish calls through the dependent API client.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter says 1.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
