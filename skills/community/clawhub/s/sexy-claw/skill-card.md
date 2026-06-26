## Description: <br>
Searches Xiaohongshu, Douyin, Bilibili, and YouTube for appearance-focused creators or videos, stores local preferences and cookies, and returns personalized recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deanzh0912](https://clawhub.ai/user/deanzh0912) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to search supported social platforms for beauty-oriented creators or videos matching stated preferences and receive ranked recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to save live social-media cookies locally, which can expose account sessions to local code that can read the skill files. <br>
Mitigation: Use an isolated environment, avoid providing active account cookies unless the exposure is acceptable, and remove or rotate cookies after use. <br>
Risk: The security scan reports unsafe shell execution paths in search scripts that could run unintended local commands. <br>
Mitigation: Review and fix shell-based search scripts before normal use, and only run the skill with trusted inputs in a least-privileged environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deanzh0912/sexy-claw) <br>
- [Publisher profile](https://clawhub.ai/user/deanzh0912) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON search-result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or update local JSON files for user preferences and platform cookies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
