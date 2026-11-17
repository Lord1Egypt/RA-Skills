## Description:

Requirement Checker uses an LLM to review requirements documents against documented quality checks and produce issue notes, source excerpts, prioritized suggestions, GWT acceptance criteria, and optional batch summary reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gotomanutd-dot](https://clawhub.ai/user/gotomanutd-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, business analysts, and development teams use this skill to check individual or batches of requirements documents for completeness, review readiness, and GWT-style acceptance criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requirement documents can be sent to the selected AI provider during checks.

Mitigation: Use a trusted or private endpoint, review the configured base_url before use, and avoid sending sensitive documents unless that endpoint is approved for the data.

Risk: API keys may be copied into the skill's local config.json.

Mitigation: Prefer environment-managed credentials when possible, restrict access to local configuration files, and rotate any key that may have been exposed.

Risk: Installation may modify the Python environment by installing dependencies.

Mitigation: Install and run the skill in an isolated environment, and review dependency-install steps before allowing global pip changes.

Risk: AI-generated issue classifications and GWT acceptance criteria may be incomplete or incorrect.

Mitigation: Have a qualified reviewer confirm generated findings and acceptance criteria before using them for formal requirements review or test planning.

## Reference(s):

- [Requirement Checker ClawHub Skill Page](https://clawhub.ai/gotomanutd-dot/skills/requirement-checker)
- [Requirement Checklist](references/checklist.md)
- [LLM Enhanced Functionality](references/llm-enhanced.md)
- [Requirements Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON check results, and interactive configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are written to the configured output directory; batch mode can produce an aggregate Markdown summary and JSON results.]

## Skill Version(s):

2.8.0 (source: server release metadata and artifact/clawhub.json; artifact/SKILL.md frontmatter says 2.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
