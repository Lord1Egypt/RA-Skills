## Description: <br>
Automates identifying trends on X (Twitter), generating opinionated content, and posting selected content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harshhmaniya](https://clawhub.ai/user/harshhmaniya) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and creators use this skill to research X trends, draft candidate posts, and publish selected content from their X account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish public X posts from the user's account without a final approval step. <br>
Mitigation: Require manual approval of the exact post text and destination account before posting. <br>
Risk: The skill uses the user's logged-in X browser session to read trends and publish posts. <br>
Mitigation: Use a dedicated browser profile or test account and confirm the active account before publication. <br>
Risk: Candidate posts and errors may be retained in memory logs. <br>
Mitigation: Review and clear the memory logs periodically. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Files, Browser actions] <br>
**Output Format:** [Text instructions, candidate post text, browser actions, and memory log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish public X posts and write candidate or error logs to memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
