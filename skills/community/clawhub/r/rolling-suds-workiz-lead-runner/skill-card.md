## Description: <br>
Read-only Rolling Suds workflow for processing Workiz leads and associated client data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mwdearing](https://clawhub.ai/user/mwdearing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators and agents use this skill to review pasted or exported Workiz lead and client data, preserve the Workiz Lead #, and route sufficiently complete records through Rolling Suds intake, estimation, and note-building workflows. It blocks estimate generation when required data such as address is missing and returns lead summaries, cleaned intake, estimates when possible, Workiz-ready notes, and manual-review flags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pasted Workiz lead and client details may contain sensitive customer data. <br>
Mitigation: Treat all pasted lead and client details as sensitive customer data and avoid sharing them outside the intended review workflow. <br>
Risk: Future Workiz API use could expand the skill from manual review into credentialed account access. <br>
Mitigation: Re-review the skill before granting Workiz API credentials, write permissions, or automated account actions. <br>
Risk: Incomplete pasted lead data can produce weak or inappropriate estimates. <br>
Mitigation: Require address before estimate generation and surface missing required data as manual-review items. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mwdearing/rolling-suds-workiz-lead-runner) <br>
- [Workiz Developer Documentation](https://developer.workiz.com) <br>
- [Default Design](references/default-design.md) <br>
- [Version History](references/version-history.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with structured lead-review sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves Workiz Lead # when provided and marks missing required data before estimation.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release metadata and artifact version history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
