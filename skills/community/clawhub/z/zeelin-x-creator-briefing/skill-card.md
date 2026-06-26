## Description: <br>
Generates AI creator briefings from recent X activity and can draft or publish summary posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelcey2023](https://clawhub.ai/user/kelcey2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, operators, and social media teams use this skill to monitor selected AI accounts, summarize notable X activity, and prepare bilingual briefings or short posts. It is intended for recurring AI trend tracking and publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated posts may be published publicly to X without a separate review step. <br>
Mitigation: Run in draft-only mode by removing publishing flags or the publish step, then review the generated post before manually publishing. <br>
Risk: Cron configuration can make the workflow publish unattended on a recurring schedule. <br>
Mitigation: Do not enable cron unless scheduled public posting is intended; disable or remove the cron task when reviewing outputs manually. <br>
Risk: Publishing depends on a separate autopost skill and whatever X account it is configured to use. <br>
Mitigation: Inspect the autopost skill and confirm the target account before allowing publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kelcey2023/zeelin-x-creator-briefing) <br>
- [Skill documentation](SKILL.md) <br>
- [README](README.md) <br>
- [Creator configuration](config/creators.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefings, short text post drafts, JSON run metadata, and command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write dated briefing and tweet-draft files, archive generated reports, and optionally publish to X when publishing is enabled.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
