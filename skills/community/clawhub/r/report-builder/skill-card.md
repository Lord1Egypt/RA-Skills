## Description: <br>
Use when the main operator needs to turn the nightly shortlist into a Telegram morning report with inline approve/reject/later buttons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omermesebuken1](https://clawhub.ai/user/omermesebuken1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators and agents use this skill to build a short morning report from shortlisted Notion ideas and send it to Telegram with approval workflow buttons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security review flagged that the skill runs local Notion pipeline code and records Telegram delivery metadata without clear disclosure. <br>
Mitigation: Review before installing, run the send script with --dry-run first, and use an isolated environment with only the required Notion and Telegram credentials. <br>
Risk: The build and send scripts depend on local paths, OpenClaw, Notion configuration, and Telegram target settings that may not exist in every environment. <br>
Mitigation: Confirm the required node and openclaw binaries, environment variables, and local paths before running the scripts. <br>


## Reference(s): <br>
- [Report schema](references/report-schema.md) <br>
- [ClawHub release page](https://clawhub.ai/omermesebuken1/report-builder) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON report payloads and Telegram message delivery commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Builds a payload file before sending and supports a dry-run send path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
