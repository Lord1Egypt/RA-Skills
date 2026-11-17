## Description:

Runs the end-to-end YouTube video workflow (research, script, visuals, assembly, metadata, upload) and stops at three mandatory human approval checkpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

Creators use this skill to take a YouTube video or Short from an idea or source material through research, scripting, visuals, editing, metadata, and upload. It requires human approval of the script, packaging, and final upload before proceeding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The status command may display stale approvals when project files are damaged or missing.

Mitigation: Require a successful --verify result for the relevant checkpoint before continuing, and personally review the script, metadata and final video at their approval checkpoints.

Risk: Approval records can be changed by someone with write access to the project state file, so they are not tamper-proof authorization.

Mitigation: Treat approvals as an audit trail and restrict write access to project files and approval state.

## Reference(s):

- [Policy notes](references/policy.md)
- [YouTube setup guide](references/setup.md)
- [YouTube channel monetization policies](https://support.google.com/youtube/answer/1311392)
- [YouTube altered or synthetic content disclosure](https://support.google.com/youtube/answer/14328491)
- [YouTube Data API quota costs](https://developers.google.com/youtube/v3/determine_quota_cost)

## Skill Output:

**Output Type(s):** [Video, Markdown, JSON configuration, Guidance]

**Output Format:** [Video file, Markdown documents, and JSON project files with user-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project files cover research, script, shot list, metadata, thumbnail, upload plan, and checkpoint status. A person must approve each of the three checkpoints.]

## Skill Version(s):

0.3.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
