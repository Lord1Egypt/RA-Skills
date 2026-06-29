## Description: <br>
Qa Team Skills provides six standardized QA assistant prompts for requirement review, test case design, agent testing, bug analysis, reporting, and team management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kokxi](https://clawhub.ai/user/kokxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers and test managers use this skill to standardize AI-assisted QA workflows across requirement review, test design, AI agent testing, defect analysis, reporting, and team management. It is intended to support human review and decision-making rather than replace QA judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: QA reports, bug exports, team metrics, and agent system prompts may contain sensitive business, personal, customer, or credential data. <br>
Mitigation: Redact secrets and personal or customer data before use, and only provide files or system prompts when organizational policy permits it. <br>
Risk: Generated QA reviews, test cases, root-cause suggestions, and management summaries can be incomplete or misleading if used without review. <br>
Mitigation: Apply the skill's human review posture for high-severity findings, P0 test cases, lower-confidence root-cause analysis, and management-facing reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kokxi/skills/qa-team-skills) <br>
- [Publisher profile](https://clawhub.ai/user/kokxi) <br>
- [skills.sh listing](https://skills.sh/Kokxi/qa-team-skills) <br>
- [README](artifact/README.md) <br>
- [User manual](artifact/docs/user-manual.md) <br>
- [Process integration guide](artifact/docs/process-integration.md) <br>
- [Changelog](artifact/docs/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration, shell commands] <br>
**Output Format:** [Markdown and structured text templates, with occasional shell commands for installation or validation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only skill; it does not directly initiate network requests or external tool execution.] <br>

## Skill Version(s): <br>
1.3.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
