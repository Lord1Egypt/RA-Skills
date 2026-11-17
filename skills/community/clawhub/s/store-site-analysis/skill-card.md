## Description:

基于高德开放平台的商铺选址分析 Skill，支持单地址竞品、配套、交通和热力图分析，以及多地址评分排名和可视化对比。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wukongmazi](https://clawhub.ai/user/wukongmazi)

### License/Terms of Use:

MIT-0

## Use Case:

External users, business analysts, and agents use this skill to evaluate candidate store locations with nearby competitors, supporting facilities, traffic conditions, and generated map-based reports. It can compare two to five addresses and return ranked recommendations for site-selection decisions.

### Deployment Geography for Use:

Global, subject to AMap service availability and applicable API key terms.

## Known Risks and Mitigations:

Risk: Generated reports can overwrite writable files when output_dir is misconfigured or controlled by an untrusted user.

Mitigation: Use a dedicated output directory with limited filesystem permissions and do not allow untrusted users to control output_dir.

Risk: AMap API keys may be exposed in generated HTML or shared reports.

Mitigation: Configure a separate browser-safe AMAP_JS_KEY and rotate AMAP_KEY if it has already appeared in shared reports.

Risk: Address strings or generated report content may allow script injection in generated HTML.

Mitigation: Run only for trusted inputs or review generated HTML before sharing it outside the execution environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wukongmazi/skills/store-site-analysis)
- [Artifact README](artifact/README.md)
- [Artifact Skill Instructions](artifact/SKILL.md)
- [AMap Open Platform](https://lbs.amap.com/)

## Skill Output:

**Output Type(s):** [text, JSON, HTML files, guidance]

**Output Format:** [JSON results with generated HTML report paths and agent-facing recommendation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AMAP_KEY and optionally AMAP_JS_KEY; writes visualization HTML files to the configured output directory.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
