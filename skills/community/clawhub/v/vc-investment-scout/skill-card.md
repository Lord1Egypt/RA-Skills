## Description: <br>
VC投资筛选工具 uses a four-layer investment screening workflow covering macro policy, industry trends, sector selection, and company fundamentals for angel, VC, growth, and M&A investment analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ksyooh](https://clawhub.ai/user/ksyooh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and investment teams use this skill to structure VC research, compare sectors, evaluate companies, generate investment recommendations, and archive reports with traceable data sources and confidence notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive investment targets, preferences, query reasons, and reports may be saved to Feishu documents and local OpenClaw memory/cache. <br>
Mitigation: Confirm Feishu document access, local storage location, retention policy, and deletion process before using the skill for confidential diligence. <br>
Risk: The skill uses local credential and cache files for paid data sources, and user controls for those files are not clearly documented. <br>
Mitigation: Confirm how API keys are supplied, who can read local memory files, and whether cached data can be disabled, cleared, or encrypted in the intended deployment. <br>
Risk: Company, policy, and industry data can fall back to public sources when paid APIs are not configured, reducing precision for investment diligence. <br>
Mitigation: Treat fallback-source results as preliminary, verify important facts against authoritative sources, and preserve the skill's confidence and source notes in final decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ksyooh/vc-investment-scout) <br>
- [Data Capability and Fallback Strategy](references/data-capability.md) <br>
- [Macro Data Sources](references/data-sources.md) <br>
- [Four-Layer Investment Screening Methodology](references/methodology.md) <br>
- [Phase 0 Preference Questions](references/phase0-questions.md) <br>
- [Company Evaluation Template](references/evaluation-template.md) <br>
- [User Methodology](references/user-methodology.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, tables, scored evaluations, archived report instructions, and occasional shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include confidence notes, source citations, investment preference context, report archive metadata, and update reminders when a newer version is detected.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
