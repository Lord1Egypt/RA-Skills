## Description:

Download and archive daily Schlagzeilen from https://www.tageblatt.de/. Use when Master asks for TAGEBLATT headlines, wants them saved locally, or needs an automated 07:00 workflow that fetches and forwards the latest headlines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zopyx](https://clawhub.ai/user/zopyx)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to fetch visible TAGEBLATT headlines, save them as local text or JSON archives, and optionally schedule a daily 07:00 workflow that forwards the latest list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The headline fetch script accepts a configurable --url value and can retrieve arbitrary URLs.

Mitigation: Use the default https://www.tageblatt.de/ URL or restrict the option before deployment; do not pass untrusted URL values.

Risk: The documented cron workflow can run recurring fetches and forward headline summaries externally through Telegram.

Mitigation: Enable automation only after confirming the schedule, destination, archive path, and sharing behavior match the intended deployment.

Risk: The artifact has no license identifier in the provided evidence.

Mitigation: Confirm license and terms before installation, redistribution, or commercial use.

## Reference(s):

- [Tageblatt Website](https://www.tageblatt.de/)
- [ClawHub Skill Page](https://clawhub.ai/zopyx/skills/tageblatt-headlines)
- [Publisher Profile](https://clawhub.ai/user/zopyx)
- [fetch_headlines.py](artifact/scripts/fetch_headlines.py)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with bash examples; generated headline archives are text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports a configurable URL, headline limit, timeout, output path, and text or JSON output format.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
