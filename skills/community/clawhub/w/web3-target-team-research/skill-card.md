## Description: <br>
Find crypto/web3 teams with $10M+ funding and verified Telegram contacts. Use when hunting for crypto leads, building contact lists, researching funded startups, or prospecting web3 companies. Spawns parallel subagent hunters to search VC portfolios and verify TG handles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shwchlorine](https://clawhub.ai/user/shwchlorine) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and go-to-market researchers use this skill to coordinate web3 lead research, identify funded crypto teams, verify individual Telegram contacts, and maintain CSV contact lists for outreach. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent autonomous hunting can continue collecting web3 lead data beyond the user's immediate request. <br>
Mitigation: Remove or tightly limit cron and auto-respawn behavior before use, and set explicit run limits and source limits. <br>
Risk: The workflow collects and stores personal Telegram contact handles in local CSV files. <br>
Mitigation: Define retention and deletion rules for contact records before running the skill, and review whether the collection is appropriate for the intended outreach. <br>
Risk: Artifact instructions include hardcoded local file paths that may write to the wrong location in another environment. <br>
Mitigation: Replace hardcoded paths with workspace-specific paths before executing commands or spawning hunters. <br>


## Reference(s): <br>
- [Web3 Target Team Research skill page](https://clawhub.ai/shwchlorine/web3-target-team-research) <br>
- [Hunter Subagent Task Template](references/hunter-task.md) <br>
- [Auto-Hunt Setup](references/auto-hunt-setup.md) <br>
- [Crypto Contact Research Workflow](references/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JavaScript tool-call examples, and CSV schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local CSV files containing researched teams and personal Telegram handles.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
