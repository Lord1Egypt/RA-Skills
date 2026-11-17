## Description:

Automatically extracts phone numbers from BOSS Zhipin chat messages and saves recruiter contact details locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[libaoming](https://clawhub.ai/user/libaoming)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers or authorized operators use this skill to extract recruiter phone numbers from BOSS Zhipin chat messages and append deduplicated contact records to a local file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects private contact data from chat messages.

Mitigation: Use it only when authorized to process the chat participants' contact data, store the output in a protected location, and delete it when no longer needed.

Risk: Unattended scans, saved sessions, proxies, or notification integrations can increase privacy and account-security exposure.

Mitigation: Avoid broad unattended scans and do not enable cron, saved-session reuse, proxies, or Telegram notifications unless those implications have been reviewed.

## Reference(s):

- [Setup Guide](references/setup.md)
- [BOSS Zhipin](https://www.zhipin.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash examples and local text-file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local append-only contact records with name, phone number, company, and timestamp when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
