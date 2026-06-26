## Description: <br>
Automates X posting through a logged-in browser session by scraping trends, generating tweet ideas, queueing approvals, and posting approved tweets without X API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nightfullstar](https://clawhub.ai/user/nightfullstar) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Creators, developers, and operators use this skill to draft and publish X posts from trends through browser automation. It supports manual posting, approval queues, scheduled workflows, and local history files for accounts already logged in to X. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act through a logged-in X session and publish posts. <br>
Mitigation: Use a dedicated browser profile or test account, keep per-post approval enabled, and avoid unattended cron or full-auto mode unless strict limits and a kill switch are added. <br>
Risk: Local queue, history, and trend files may contain account activity or generated content. <br>
Mitigation: Review local data files regularly, keep data/ excluded from version control, and remove sensitive drafts or history before sharing the skill directory. <br>
Risk: The security review flags weak guardrails around automated social posting. <br>
Mitigation: Set conservative daily limits, review every generated post before publication, and do not rely on credential-free or Terms of Service claims as security guarantees. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nightfullstar/x-automation) <br>
- [Publisher profile](https://clawhub.ai/user/nightfullstar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON cron configuration, local JSON data files, and browser automation actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local trend, queue, approval, and tweet-history JSON files under data/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
