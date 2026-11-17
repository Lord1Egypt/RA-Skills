## Description:

Guides agents in creating traceable ecommerce Listing, PDP, and detail-page short-video tasks with Seedance 2.5 through AI Hive, where each clip answers one purchase question such as in-box contents, dimensions, compatibility, setup, material details, SKU variants, or feature evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, marketers, and agents use this skill to prepare fact-bound product-video generation tasks for marketplace listings and PDP modules. It helps structure approved product images, motion references, facts, platform constraints, and rejection criteria before submitting jobs to AI Hive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an external AI Hive service and may upload selected product images or videos.

Mitigation: Install only if the AI Hive service is trusted, avoid sensitive assets when possible, and keep the API key scoped and protected.

Risk: The security summary reports a transport-validation weakness that could expose selected product media or write oversized or untrusted downloads if the API or storage endpoint redirects unexpectedly.

Mitigation: Run with --preview first, use --no-download when only a task ID is needed, and consider dependency pinning or isolated execution before processing sensitive product assets.

Risk: Generated clips could imply unsupported product claims if source facts, platform rules, or visual outputs are not reviewed.

Mitigation: Review each generated clip against approved SKU records, fact sources, platform policies, and the skill's acceptance checks before publication.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wubin1836/skills/seedance-2-5-ecommerce-video)
- [AI Hive OpenAPI endpoint](https://ai-hive.iclip.cn/api/openapi/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code]

**Output Format:** [Markdown guidance with inline bash commands and JSON preview/status output from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload selected product images or videos to AI Hive and may download generated MP4 results unless preview or no-download modes are used.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
