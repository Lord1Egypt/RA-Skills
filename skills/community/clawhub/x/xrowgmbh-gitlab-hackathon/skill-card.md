## Description: <br>
Plan and execute fair GitLab hackathon participation, including Quarterly and Transcend Hackathons, by analyzing rules, selecting qualifying issues and merge requests, tracking scoring levers, and keeping an exploit watchlist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xrowgmbh](https://clawhub.ai/user/xrowgmbh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external contributors use this skill to plan fair GitLab hackathon participation, select reviewable issues and merge requests, verify current rules, and avoid scoring behavior that could burden maintainers or violate event expectations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent toward GitLab actions such as creating, labeling, closing, commenting on issues, or opening merge requests. <br>
Mitigation: Use a minimally scoped GitLab token and review proposed GitLab actions before execution. <br>
Risk: Hackathon rules, scoring values, dates, registration requirements, and prize criteria can change. <br>
Mitigation: Verify current GitLab hackathon rules and contribution point documentation before optimizing work. <br>
Risk: Point-focused activity can become spammy or unfair if comments, labels, closures, commits, or submissions are padded. <br>
Mitigation: Limit activity to legitimate contributions, keep merge requests reviewable, and avoid exploit-like behavior unless maintainers explicitly approve it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xrowgmbh/skills/xrowgmbh-gitlab-hackathon) <br>
- [GitLab Quarterly Hackathon](https://contributors.gitlab.com/hackathon) <br>
- [Current Hackathon API](https://contributors.gitlab.com/api/v1/hackathons/current) <br>
- [GitLab Transcend Hackathon](https://contributors.gitlab.com/transcend-hackathon) <br>
- [GitLab Contribution Points](https://contributors.gitlab.com/docs/user-guide#contribution-points) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires glab, jq, curl, and a minimally scoped GITLAB_TOKEN for GitLab operations.] <br>

## Skill Version(s): <br>
1.62.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
