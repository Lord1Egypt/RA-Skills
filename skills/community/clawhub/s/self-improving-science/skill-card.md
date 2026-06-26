## Description: <br>
Captures learnings, experiment issues, and methodology corrections for continuous improvement in scientific research and ML workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jose-compu](https://clawhub.ai/user/jose-compu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, data scientists, and ML engineers use this skill to record methodological corrections, experiment failures, reproducibility issues, data quality findings, and tooling requests so future experiments can account for them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Learning logs may capture sensitive research data, credentials, patient data, proprietary samples, or raw datasets. <br>
Mitigation: Keep entries to summary statistics and redacted excerpts, and avoid storing credentials, patient identifiers, proprietary samples, or raw datasets. <br>
Risk: Global hook matchers can make reminders appear in contexts where the skill is not relevant. <br>
Mitigation: Prefer project-level scoped hook matchers and enable hooks only when the local research-memory workflow is desired. <br>
Risk: Promoted learnings may persist incorrect or misleading guidance in project governance or model documentation. <br>
Mitigation: Review proposed changes to AGENTS.md, SOUL.md, TOOLS.md, model cards, and governance documents before allowing them to persist. <br>
Risk: Cross-session sharing can expose information outside the intended session context. <br>
Mitigation: Use cross-session sharing only in trusted environments and send concise findings or summary statistics rather than raw datasets, credentials, or full notebooks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jose-compu/self-improving-science) <br>
- [Entry Examples](references/examples.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local .learnings markdown entries; optional hooks emit reminder text.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
