## Description: <br>
Searches Xiaohongshu keywords, collects matching note URLs, extracts note text, engagement counts, and visible comments, then helps an agent summarize trends, sentiment, topics, or product feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ligoudanblabla](https://clawhub.ai/user/ligoudanblabla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to research Xiaohongshu keywords, collect public note content and comments, and turn the results into concise trend, sentiment, topic, or product-feedback summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AgentBay API keys may be exposed in plaintext logs. <br>
Mitigation: Remove API-key logging before use, rotate any key used during testing, and avoid installing this version with sensitive AgentBay credentials. <br>
Risk: Xiaohongshu login cookies persist in the AgentBay browser context. <br>
Mitigation: Use a non-sensitive account where appropriate and clear the browser context or cookies after completing a task. <br>
Risk: Extracted notes, comments, status, and logs remain on local disk until cleanup. <br>
Mitigation: Delete local output, status, and log artifacts after review, and avoid sharing logs or intermediate files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ligoudanblabla/xhs-search-skill) <br>
- [AgentBay service](https://www.aliyun.com/product/agentbay) <br>
- [Xiaohongshu](https://www.xiaohongshu.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and structured analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Intermediate search URL files, extracted note JSON, status, and logs are local operational artifacts and should not be shown as end-user output.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
