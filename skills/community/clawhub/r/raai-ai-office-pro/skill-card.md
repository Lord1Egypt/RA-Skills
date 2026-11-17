## Description:

Operational chief-of-staff for Russian CEOs: OKR, weekly review, decision log, briefing, delegation and strategic priorities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raaipro](https://clawhub.ai/user/raaipro)

### License/Terms of Use:

MIT-0

## Use Case:

External Russian-speaking CEOs, owners, and managing directors use this skill to structure operating rhythms around OKRs, daily briefings, weekly reviews, decision logs, delegation, investor updates, and strategic priorities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package security verdict is suspicious, and the server summary says the main CEO assistant is coherent but includes under-scoped helper prompts and scripts that need review.

Mitigation: Review the package before installation, especially SKILL.md, config/raai_system_prompt.md, install.sh, build.sh, and test/smoke-test.sh.

Risk: Bundled shell scripts fail static shell syntax checks and the security guidance says exact file writes and a manual or dry-run install path are not documented.

Mitigation: Avoid running bundled shell scripts until the publisher fixes syntax errors, documents file writes, supplies a manual or dry-run install path, and provides the expected environment template.

Risk: Optional integrations can expose business spreadsheets, calendar events, decision logs, and Russian-language business operating data.

Mitigation: Keep integrations disabled unless explicitly needed, use least-privilege credentials, and test with non-sensitive data before connecting production systems.

Risk: The skill can produce misleading operating recommendations when KPI, calendar, delegation, or decision data is missing or inaccurate.

Mitigation: Require CEO or operator review of outputs and populate configuration and metrics with real, current business data before relying on the generated plans.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/raaipro/skills/raai-ai-office-pro)
- [README](artifact/README.md)
- [Quick Start](artifact/examples/quick-start.md)
- [Onboarding](artifact/docs/onboarding.md)
- [Anti-Fail Limitations](artifact/docs/anti-fail.md)
- [ROI](artifact/docs/roi.md)
- [Dogfooding Proof](artifact/proof/dogfooding-RAAI.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration, shell commands]

**Output Format:** [Markdown with structured business templates and occasional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Russian-language management outputs; quality depends on user-provided business data and enabled integrations.]

## Skill Version(s):

3.5.4 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
