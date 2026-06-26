## Description: <br>
Downloads and archives daily public headlines from tageblatt.de for local headline lists, archives, and optional scheduled forwarding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zopyx](https://clawhub.ai/user/zopyx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users and agents use this skill to fetch the latest public Tageblatt headlines, save them as text or JSON, and support an optional daily 07:00 headline workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch URLs beyond the intended Tageblatt site when a custom URL is supplied. <br>
Mitigation: Restrict routine use to https://www.tageblatt.de/ and confirm any alternate URL before execution. <br>
Risk: The skill can write headline output to user-selected file paths. <br>
Mitigation: Use a known archive directory for outputs and review requested paths before running scheduled jobs. <br>
Risk: Scheduled Telegram forwarding may distribute fetched headline data automatically. <br>
Mitigation: Require explicit confirmation before enabling scheduling or Telegram forwarding. <br>


## Reference(s): <br>
- [Tageblatt source site](https://www.tageblatt.de/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [Plain text or JSON headline lists, with Markdown and bash examples in the skill guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write to a user-selected output path and can be scheduled for daily execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
