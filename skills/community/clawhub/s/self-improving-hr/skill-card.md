## Description: <br>
Captures policy gaps, compliance risks, recruiting process issues, onboarding friction, retention signals, candidate experience problems, and offboarding gaps to enable continuous HR improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jose-compu](https://clawhub.ai/user/jose-compu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR and people-operations teams use this agent skill to capture anonymized HR process learnings, compliance risks, candidate experience issues, onboarding friction, and retention patterns. The captured Markdown logs can inform policy updates, onboarding checklists, interview scorecards, compliance calendars, and HR workflow improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive HR context and persistent learning logs may accidentally capture employee or candidate personal data. <br>
Mitigation: Keep .learnings local and out of version control, do not store PII or confidential employee details, and anonymize examples before logging. <br>
Risk: Broad always-on hooks can add HR reminders or inspect Bash output in sessions where the HR workflow is not intended. <br>
Mitigation: Use project-local hooks with HR-specific matchers, enable the optional hook workflow intentionally, and avoid the Bash output detector unless it is necessary. <br>
Risk: Generated policy, AGENTS.md, or extracted-skill changes could introduce incorrect HR guidance. <br>
Mitigation: Manually review proposed policy, AGENTS.md, and generated-skill changes before accepting them, especially for compliance-sensitive content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jose-compu/self-improving-hr) <br>
- [Entry Examples](references/examples.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes or proposes project-local .learnings Markdown entries and optional HR skill scaffolds; no external API keys are required by the artifact evidence.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
