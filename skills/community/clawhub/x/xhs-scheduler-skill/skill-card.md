## Description: <br>
小红书智能排期发布器 helps content creators manage Xiaohongshu content queues, recommend posting times, and schedule automated publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sxzxlj](https://clawhub.ai/user/sxzxlj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content creators, MCN operators, and brand content teams use this skill to queue Xiaohongshu posts, choose suggested posting times, run scheduled publishing, and monitor publishing outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish queued Xiaohongshu posts from a logged-in account. <br>
Mitigation: Review the queue before starting the scheduler, keep conservative rate limits, and use it only with accounts you are authorized to operate. <br>
Risk: Configured notification webhooks may send status data to external services. <br>
Mitigation: Configure webhooks only for destinations you control and avoid placing sensitive content in notification payloads. <br>
Risk: The skill depends on the external xiaohongshu-mcp service and Python packages. <br>
Mitigation: Inspect or pin the MCP service and Python dependencies before using the skill with a real account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sxzxlj/xhs-scheduler-skill) <br>
- [Publisher profile](https://clawhub.ai/user/sxzxlj) <br>
- [README](artifact/README.md) <br>
- [SKILL definition](artifact/SKILL.md) <br>
- [Xiaohongshu MCP service](https://github.com/xpzouying/xiaohongshu-mcp.git) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, markdown] <br>
**Output Format:** [Markdown instructions with command examples and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local Python scripts, a local Xiaohongshu MCP service, and optional notification webhooks when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact frontmatter, and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
