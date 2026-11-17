## Description: <br>
安全情报雷达聚合 NVD CVE、GitHub Security Advisory 和社区安全通报，并按资产关联度与可利用性优先级筛选安全告警。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security operators, and agent maintainers use this skill to monitor vulnerability and threat intelligence feeds, correlate advisories with installed skills or dependencies, and receive prioritized alert summaries or reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A configured feed URL may provide incorrect or untrusted advisory content. <br>
Mitigation: Use a trusted feed source or internal mirror, and review feed configuration before enabling automated alert workflows. <br>
Risk: Local skill and dependency inventories may reveal sensitive environment details. <br>
Mitigation: Store inventories under user-controlled paths with restrictive permissions and include only the assets needed for matching advisories. <br>
Risk: Cache and state files may retain historical advisory and asset-matching data. <br>
Mitigation: Protect the cache and state directory, rotate or clear stale files when no longer needed, and review retained data before sharing logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/security-radar) <br>
- [NVD CVE API](https://services.nvd.nist.gov/rest/json/cves/2.0) <br>
- [GitHub Security Advisory API](https://api.github.com/advisories) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text alert/status messages and Markdown reports with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local asset inventory, cache, and state files to deduplicate advisories and support offline snapshots.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
