## Description: <br>
OpenClaw Swarm Layer turns workflow specifications into executable task graphs, then helps agents plan, run, review, diagnose, and report local project workflows through manual or ACP-backed execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xucheng](https://clawhub.ai/user/xucheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to turn Markdown workflow specs into task plans, dispatch work through OpenClaw runners, manage review gates, recover stuck sessions, and generate local or Obsidian-synced progress reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ACP autopilot and watcher mode can keep dispatching or ticking workflow tasks after setup. <br>
Mitigation: Use dry-run and status commands first, confirm pause and stop controls, and keep review gates enabled for work that needs operator approval. <br>
Risk: Local reporting and optional Obsidian sync can copy project details into report destinations. <br>
Mitigation: Enable Obsidian sync or generated reports only for trusted, access-controlled locations, especially when projects contain sensitive information. <br>
Risk: Workflow automation can leave tasks blocked, stuck, or exhausted after retries. <br>
Mitigation: Use doctor, status, session cancel, cleanup, and dead-letter review flows before resuming automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xucheng/swarm-layer) <br>
- [GitHub repository](https://github.com/xucheng/openclaw-swarm-layer) <br>
- [npm package](https://www.npmjs.com/package/openclaw-swarm-layer) <br>
- [Documentation](https://github.com/xucheng/openclaw-swarm-layer/tree/main/docs) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown, text] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, task instructions, and report descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct OpenClaw to create or update local workflow state, reports, run logs, review logs, spec archives, completion summaries, and optional Obsidian mirrors.] <br>

## Skill Version(s): <br>
0.5.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
