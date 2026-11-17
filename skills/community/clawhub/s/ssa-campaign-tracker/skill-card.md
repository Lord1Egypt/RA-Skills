## Description:

Campaign Tracker helps agents archive outbound email records, match customer replies, generate campaign performance reports, and suggest email template optimizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and growth teams use this skill to track outbound email campaign activity, connect sent messages to replies, and produce weekly or monthly performance summaries. Developers or operators can also use it to maintain local campaign tracking data and generate template optimization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes email and customer campaign data and writes local archives, tracking files, reports, and logs.

Mitigation: Use a dedicated, least-privileged mailbox or export directory and keep outputs in a private location.

Risk: Under-scoped local writes or untrusted email-derived values could affect campaign tracking files or report paths.

Mitigation: Run dry-run mode first, set OBSIDIAN_VAULT deliberately, and validate campaign IDs and report filenames before processing untrusted data.

## Reference(s):

- [Campaign Tracker ClawHub Skill Page](https://clawhub.ai/cjboy007/skills/ssa-campaign-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, JSONL, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run execution and optional Obsidian Markdown output.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
