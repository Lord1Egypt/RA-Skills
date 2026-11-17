## Description:

Summarizes conversation text into professional PowerPoint or WPS presentation files, with fully local processing and optional Feishu upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to turn conversation notes, meetings, learning notes, and project updates into shareable presentation files. Users can keep processing local or intentionally enable Feishu upload for tenant sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Feishu upload can send generated presentation data to a Feishu tenant when credentials and upload mode are enabled.

Mitigation: Use local mode by leaving Feishu disabled and withholding FEISHU_APP_ID and FEISHU_APP_SECRET unless uploads are intentional.

Risk: Network checks and upload paths may create network traffic.

Mitigation: Do not run the permission checker when zero network traffic is required; validate the skill in an isolated environment first.

Risk: WPS AppleScript automation needs review before use with untrusted conversation text.

Mitigation: Avoid WPS AppleScript mode for untrusted input; prefer local PowerPoint or python-pptx generation.

Risk: Saved Feishu credentials can persist in configuration files or shell startup files.

Mitigation: Prefer temporary environment variables or a credential manager instead of saving secrets in config files or shell startup files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwumit/skills/sum2slides-lite)
- [User guide](docs/USER_GUIDE.md)
- [Security guide](docs/SECURITY_GUIDE.md)
- [Operational risks](docs/OPERATIONAL_RISKS.md)
- [Platform compatibility](docs/PLATFORM_COMPATIBILITY.md)

## Skill Output:

**Output Type(s):** [Files, Configuration, Guidance]

**Output Format:** [PowerPoint .pptx files with optional Feishu upload link and Markdown-style guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local mode avoids network use; Feishu upload mode requires user-provided credentials.]

## Skill Version(s):

1.1.6 (source: server release metadata, SKILL.md, VERSION.txt)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
