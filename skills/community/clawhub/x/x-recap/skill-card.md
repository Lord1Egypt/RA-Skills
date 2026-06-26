## Description: <br>
Monitor and recap official X (Twitter) updates using actionbook-rs screenshots when tracking X posts, especially official accounts, setting up cron-based X monitoring, troubleshooting X login or blank timelines, or standardizing a fetch, screenshot, and recap workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jack4world](https://clawhub.ai/user/jack4world) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to capture official X account screenshots with actionbook-rs and produce concise recaps of notable updates. It also supports cron setup and troubleshooting for X monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens X pages with a local browser profile and writes screenshots that may capture account-visible content. <br>
Mitigation: Use only the intended X browser profile, avoid private sessions unless acceptable, and review screenshot output before sharing. <br>
Risk: X timelines can be blank, spinner-only, rate-limited, or inconsistent across runs. <br>
Mitigation: Re-login when screenshots are blank, reduce fetch frequency when rate limits or bot detection appear, and verify screenshot content before relying on a recap. <br>
Risk: Cron payloads can drift from the bundled fetch scripts and produce inconsistent captures. <br>
Mitigation: Keep fetch logic in the bundled scripts and configure cron jobs to call those scripts before recapping screenshots. <br>


## Reference(s): <br>
- [X Recap runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise recap text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference locally generated screenshot files and output directories.] <br>

## Skill Version(s): <br>
2026.2.25 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
