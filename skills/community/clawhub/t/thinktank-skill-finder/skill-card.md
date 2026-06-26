## Description: <br>
ThinkTank Skill Finder helps agents search, recommend, compare, and install ClawHub skills and research-focused skill bundles for think tank, academic, monitoring, report-writing, visualization, PDF, table, and presentation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sapereaude2014](https://clawhub.ai/user/sapereaude2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and agent operators use this skill to find individual ClawHub skills or install curated research bundles for information gathering, document processing, analysis, visualization, and report delivery. It supports both one-off recommendations and bundle installation workflows, with restricted mode as the default bundle posture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundle installation persistently adds selected third-party skills to the agent environment. <br>
Mitigation: Review the listed skills before installation and remove unwanted skills from the target skills directory after testing. <br>
Risk: Standard mode may include skills that require API keys, external services, or network access outside the default restricted posture. <br>
Mitigation: Use restricted mode unless those dependencies are intentional and credentials are approved for the environment. <br>
Risk: Installed skills may influence future agent behavior after the current task ends. <br>
Mitigation: Install into a scoped workdir when evaluating bundles and verify the final skill list with the provided inspect or list commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sapereaude2014/thinktank-skill-finder) <br>
- [Publisher profile](https://clawhub.ai/user/sapereaude2014) <br>
- [ClawHub mirror registry](https://cn.clawhub-mirror.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with concise recommendation lists and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include skill names, Chinese descriptions, download and star counts, installed status, bundle names, install commands, and verification commands.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence; matches artifact H1 and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
