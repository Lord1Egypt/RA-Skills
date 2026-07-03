## Description: <br>
Analyzes fixed-camera home video of elders living alone to identify behavior indicators such as prolonged dazing, sighing, and self-talking, then returns behavior statistics and an emotional-risk report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External caregivers, family members, and community care workers use this skill to analyze consented elder home-video inputs for non-diagnostic behavioral risk signals and to review generated reports or historical report lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends highly sensitive elder home-video inputs, derived risk reports, identity information, and report-history queries to external Life Emergence services. <br>
Mitigation: Use only with explicit consent from the monitored elder or lawful guardian, confirm acceptable retention and access controls before installation, and avoid third-party videos or contexts where consent cannot be verified. <br>
Risk: The skill silently creates or reuses identity records and stores tokens locally. <br>
Mitigation: Install only where silent identity reuse and local token storage are acceptable, and restrict host access to trusted operators. <br>
Risk: Behavioral indicators can be confused with benign activities and the output could be mistaken for a medical diagnosis. <br>
Mitigation: Treat reports as non-diagnostic behavioral risk prompts; use clinical screening or qualified medical review for diagnosis, treatment, or urgent safety decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-elderly-loneliness-depression-analysis) <br>
- [API documentation](references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Text or Markdown summaries with optional JSON report output and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query cloud-hosted historical reports and may save result text to a user-specified output file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
