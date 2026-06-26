## Description: <br>
Adaptive skill scheduling engine with environment-aware routing, user preferences, and self-learning optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[namechenxinyu](https://clawhub.ai/user/namechenxinyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Skill Pilot to route prompts to installed skills, compare candidate tools in full mode, and tune defaults using environment signals, user preferences, and execution history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run other installed skills with inherited environment variables. <br>
Mitigation: Use it only with trusted installed skills, run it in an isolated environment when possible, and expose only the minimum API keys needed for the current task. <br>
Risk: Sensitive prompts or execution details may be persisted in local Skill Pilot history and config files. <br>
Mitigation: Avoid routing highly sensitive prompts through the skill unless necessary, and periodically inspect or clear the ~/.openclaw skill-pilot history and config files. <br>
Risk: The skill may choose different tools based on environment and learned history, which can affect result consistency. <br>
Mitigation: Use full mode for important tasks to compare candidate tools, review the selected result, and reset or edit defaults when routing behavior is not appropriate. <br>


## Reference(s): <br>
- [Capability Taxonomy](references/capability-taxonomy.md) <br>
- [Micro Routing Examples](references/micro-routing-examples.md) <br>
- [Reminder Policy](references/reminder-policy.md) <br>
- [Resolution Order](references/resolution-order.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/namechenxinyu/skill-pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with optional inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include concise routed results, source labels, tool comparison reports, default-tool updates, health summaries, or observability reports.] <br>

## Skill Version(s): <br>
0.4.6 (source: frontmatter, package.json, ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
