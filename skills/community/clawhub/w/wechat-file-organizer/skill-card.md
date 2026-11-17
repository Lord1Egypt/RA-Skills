## Description:

Scans local WeChat received-file folders, reports file usage and duplicates, and optionally copies files into type- or month-based folders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

People or agents managing locally received WeChat files can review storage and duplicate reports, then optionally organize files across detected folders and accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanning WeChat folders reads local file metadata and contents for hashes.

Mitigation: Run only on folders you intend to inspect; review the default dry-run report and paths first.

Risk: Applying changes creates copies, and using --trash moves originals to the recycle bin.

Mitigation: Use --apply or --trash only after checking the proposed sources and destination.

## Reference(s):

- [WeChat File Organizer on ClawHub](https://clawhub.ai/oracis/skills/wechat-file-organizer)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [Plain-text report or JSON; organized file copies when explicitly applied]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can identify source accounts; the default dry-run does not change files.]

## Skill Version(s):

2.1.0 (source: ClawHub release, skill frontmatter, manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
