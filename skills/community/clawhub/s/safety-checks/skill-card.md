## Description: <br>
Verify before you trust - model pinning, fallbacks, and runtime safety validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to run local pre-flight safety checks for model version drift, fallback configuration, cache staleness, and cross-session state hygiene before relying on an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fallback checks audit configured entries only and do not prove live network connectivity or model availability. <br>
Mitigation: Treat fallback results as configuration validation and separately test real connectivity before depending on degraded-mode paths. <br>
Risk: The --clear and --clear-state options can remove local cache or session-state files. <br>
Mitigation: Use clearing options only when you intend to remove the skill's local cache or session-state artifacts. <br>
Risk: Companion skills may introduce separate behavior or risk outside this skill's local-only safety checks. <br>
Mitigation: Review and scan companion skills independently before relying on integrated enforcement workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/leegitw/safety-checks) <br>
- [Publisher profile](https://clawhub.ai/user/leegitw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown-style check reports with command examples and YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local check results and history under output/safety/ when checks are performed.] <br>

## Skill Version(s): <br>
1.5.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
