## Description: <br>
X hourly growth ops skill for finding AI/builder follow-back or mutual-connect posts, leaving high-quality English replies through the logged-in Chrome browser, and running on a daily hourly schedule with dedupe, safety filters, and daily caps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelcey2023](https://clawhub.ai/user/kelcey2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and growth operators use this skill to find relevant X follow-back or mutual-connect posts, post concise replies from a logged-in OpenClaw Chrome profile, and maintain dedupe and daily posting limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can repeatedly post public replies from the logged-in X account. <br>
Mitigation: Start with --dry-run, verify the target account and generated replies, and lower max-comments or daily caps before enabling posting. <br>
Risk: The LaunchAgent can run hourly in the background using broad browser control. <br>
Mitigation: Use a dedicated OpenClaw Chrome profile where possible and uninstall the LaunchAgent when unattended posting is no longer intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kelcey2023/zeelin-x-hourly-growth) <br>
- [Publisher profile](https://clawhub.ai/user/kelcey2023) <br>
- [Comment templates](references/comment-templates.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash commands and optional JSON dry-run output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Posts public X replies through the logged-in browser profile unless run with --dry-run.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
