## Description: <br>
DeepLink Agentic helps agents create, monitor, retrieve, and refine real-estate research tasks through the agentic.dichanai.com service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shirleydddd](https://clawhub.ai/user/shirleydddd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Real-estate analysts, operators, and agents use this skill to delegate complex property market, land, enterprise, policy, project, and property-management research tasks to DeepLink Agentic, then monitor progress and retrieve deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and user-selected reference files are sent to agentic.dichanai.com for task execution. <br>
Mitigation: Send only approved inputs and avoid including sensitive data unless the user trusts the service for that data. <br>
Risk: The skill handles AGENTIC_TOKEN and may print a renewed token as NEW_TOKEN. <br>
Mitigation: Use limited or short-lived tokens where possible and never share terminal output that contains NEW_TOKEN. <br>
Risk: Delete and share commands can remove remote tasks or make task contents publicly accessible. <br>
Mitigation: Confirm user intent before running delete or share operations and treat them as high-impact actions. <br>


## Reference(s): <br>
- [DeepLink Agentic on ClawHub](https://clawhub.ai/shirleydddd/realestate-deep-research) <br>
- [DeepLink Agentic Service](https://agentic.dichanai.com) <br>
- [DeepLink Agentic API Documentation](https://agentic.apifox.cn/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and service-generated task or file links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the requests package, and AGENTIC_TOKEN; may send user prompts and selected files to agentic.dichanai.com.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
