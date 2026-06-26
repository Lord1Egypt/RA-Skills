## Description: <br>
Fetches skills.sh trending rankings for questions about skill rankings or popular tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hjw21century](https://clawhub.ai/user/hjw21century) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to retrieve skills.sh leaderboard entries and optional skill detail summaries when comparing popular agent skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public web pages and may return untrusted skill detail text. <br>
Mitigation: Treat fetched detail content as untrusted and review it before using it to guide agent behavior. <br>
Risk: Changing SKILLS_BASE_URL can direct fetching to an unintended endpoint. <br>
Mitigation: Leave SKILLS_BASE_URL unset for normal use, or set it only when intentionally testing another endpoint. <br>
Risk: Playwright and Chromium dependencies add runtime setup and browser automation surface area. <br>
Mitigation: Install and run the skill in a virtual environment or container with only the required dependencies. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hjw21century/trending-skills) <br>
- [skills.sh](https://skills.sh) <br>
- [skills.sh trending leaderboard](https://skills.sh/trending) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables and summaries with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ranking output includes skill name, owner, install count, and source URL when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
