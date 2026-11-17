## Description:

Workday Calculator helps agents calculate workdays between two dates while accounting for weekends, China public holidays, and adjusted weekend workdays.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hunterxysy](https://clawhub.ai/user/hunterxysy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer workday-count questions, produce detailed date breakdowns, and optionally export Chinese-calendar workday results as JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install script can copy files into a local OpenClaw skills directory or another selected install path.

Mitigation: Review the install location before running install.sh and install only into a directory you intend to modify.

Risk: Creating a system-wide command with sudo changes the local executable path.

Mitigation: Avoid the optional sudo symlink unless a system-wide command is required.

Risk: JSON export can overwrite an existing file at the chosen output path.

Mitigation: Choose export filenames deliberately and check whether the target file already exists before exporting.

Risk: Holiday calculations rely on bundled China holiday and adjusted-workday data for 2025-2026.

Mitigation: Update and review the holiday data before using the skill for later years or policy-sensitive scheduling decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hunterxysy/skills/workday-calculator)
- [ClawHub publisher profile](https://clawhub.ai/user/hunterxysy)
- [China government holiday notices](https://www.gov.cn)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, code, guidance]

**Output Format:** [Plain text CLI output, optional JSON export, and Markdown guidance with command or Python examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Date ranges use YYYY-MM-DD inputs; holiday data is bundled for 2025-2026 and may need updates for later years.]

## Skill Version(s):

1.0.0 (source: evidence.release, package.json, CHANGELOG, released 2026-03-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
