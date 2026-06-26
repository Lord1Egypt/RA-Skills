## Description: <br>
抓取 Solidot 热门和最新文章，推送到飞书。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[n0nsense11](https://clawhub.ai/user/n0nsense11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and personal automation users use this skill to collect Solidot headlines and publish them to a Feishu document or local Markdown file for daily reading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Feishu document token can grant write access to the target document. <br>
Mitigation: Use a token scoped to the intended document and keep it out of shared logs or prompts. <br>
Risk: When no Feishu token is configured, the skill writes $WORKSPACE/solidot-push.md and may replace an existing file at that path. <br>
Mitigation: Run it in the intended workspace and preserve any existing file before execution if its contents matter. <br>
Risk: The optional cron example runs the skill on a recurring daily schedule. <br>
Mitigation: Add the cron job only when daily execution is desired, and remove or disable it when the automation is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/n0nsense11/solidot-push) <br>
- [Solidot](https://www.solidot.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown document with article titles and links, plus command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to Feishu when FEISHU_DOC_TOKEN is set; otherwise writes $WORKSPACE/solidot-push.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
