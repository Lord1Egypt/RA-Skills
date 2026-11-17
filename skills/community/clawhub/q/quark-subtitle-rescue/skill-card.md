## Description:

Bulk add subtitles to Quark movie folders with high success and low wrong-match risk. Best for "all subfolders" jobs, interrupted runs, and retrying failed titles with multi-source fallback (OpenSubtitles/SubHD/YIFY), strict matching, rollback safety, and completion reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangqi00987](https://clawhub.ai/user/tangqi00987)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to recover or complete subtitle uploads across many Quark movie folders, especially after interrupted runs or failed matches. It guides staged retries, provider fallback, rollback checks, and completion reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides an agent to run subtitle tooling against a user's Quark account, so mishandled credentials or account context could expose sensitive access.

Mitigation: Confirm trust in the existing quark_subtitle_tool before installation, store the Quark cookie securely, and do not paste or print it.

Risk: Batch subtitle workflows can upload wrong matches or require rollback deletes in cloud storage.

Mitigation: Review batch results before accepting uploads or rollback deletes, and use the skill's spot-check and rollback guidance before declaring completion.

## Reference(s):

- [Workflow Reference](references/workflow.md)
- [Troubleshooting](references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/tangqi00987/skills/quark-subtitle-rescue)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes staged workflow decisions, safety checks, troubleshooting guidance, and completion report commands.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
