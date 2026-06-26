## Description: <br>
Captures marketing performance issues, reusable campaign learnings, feature requests, and promotion candidates so agents can support continuous marketing improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jose-compu](https://clawhub.ai/user/jose-compu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators and agent users use this skill to capture campaign issues, messaging misses, channel underperformance, audience drift, attribution gaps, brand inconsistency, content decay, and marketing tooling requests. The skill helps convert recurring patterns into brand guidelines, channel playbooks, personas, attribution standards, or new marketing skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hook examples with broad or empty matchers can inject reminders outside marketing work. <br>
Mitigation: Keep hooks project-level and narrow matchers to marketing-specific terms before enabling them. <br>
Risk: Marketing learning files could capture secrets, customer PII, ad account credentials, or sensitive revenue details. <br>
Mitigation: Record only aggregated metrics and redacted campaign identifiers; do not store secrets or sensitive customer and revenue data. <br>
Risk: PostToolUse hooks may inspect local command output that contains sensitive information. <br>
Mitigation: Enable PostToolUse only when command-output inspection is needed, and review generated skill output before trusting or deploying it. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/jose-compu/self-improving-marketing) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, hook configuration examples, and structured markdown log templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local .learnings markdown files and optional hook-related skill scaffolds when the user chooses to apply the guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
