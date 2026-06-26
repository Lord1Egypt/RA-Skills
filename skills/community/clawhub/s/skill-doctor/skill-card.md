## Description: <br>
Diagnoses the health of published ClawHub skills and plugins, then prescribes concrete next actions for portfolio health, growth, moderation, conversion, and maintenance signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[welove111](https://clawhub.ai/user/welove111) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and ClawHub publishers use Skill Doctor to review one listing or an entire portfolio, identify weak adoption or trust signals, and receive prioritized next actions. It can run deterministic local diagnostics, produce Markdown check-up reports, and optionally add AI-narrated analysis when the user explicitly enables the Anthropic integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads configured ClawHub skill and plugin metrics and stores local history under ~/.skill-doctor. <br>
Mitigation: Use it only for listings you intend to monitor, review the configured slugs and plugins, and remove local history when it is no longer needed. <br>
Risk: The optional --deep mode sends compact portfolio diagnostics to Anthropic when an API key is configured. <br>
Mitigation: Leave --deep disabled unless external AI analysis is acceptable, and avoid storing the Anthropic API key on shared machines. <br>


## Reference(s): <br>
- [Diagnostic Rules](references/diagnostic-rules.md) <br>
- [Deep Analysis Setup](references/deep-analysis-setup.md) <br>
- [Skill Doctor ClawHub Listing](https://clawhub.ai/welove111/skill-doctor) <br>
- [Anthropic Console](https://console.anthropic.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown check-up report with structured findings and prescriptions; optional PNG trend chart file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local state under ~/.skill-doctor for trend comparison; optional deep analysis sends compact diagnostic metrics only when explicitly enabled.] <br>

## Skill Version(s): <br>
1.0.3 (source: SKILL.md frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
