## Description: <br>
Cut your LLM costs by 200x. Offload parallel, batch, and research work to Gemini Flash workers instead of burning your expensive primary model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Chair4ce](https://clawhub.ai/user/Chair4ce) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use Swarm to run independent prompts, research tasks, batch jobs, structured extraction, voting, and multi-stage analysis through local CLI and HTTP daemon workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local LLM orchestration daemon with provider API keys and outbound network access. <br>
Mitigation: Install only in trusted environments, bind services to localhost or firewall them, and avoid sending secrets or regulated data in prompts. <br>
Risk: Prompt data, cache entries, metrics, and configuration may be stored under the user's local Clawdbot configuration directory. <br>
Mitigation: Review stored files under ~/.config/clawdbot, periodically clear cache and metrics, and disable caching for sensitive tasks. <br>
Risk: Docker cluster mode and benchmark scripts can expose task APIs or consume provider quota. <br>
Mitigation: Use Docker cluster mode and benchmarks only on controlled networks with clear quota limits and monitoring. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Chair4ce/swarm) <br>
- [Skill Instructions](SKILL.md) <br>
- [README](README.md) <br>
- [Install Guide](INSTALL.md) <br>
- [Roadmap](docs/ROADMAP.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown, JSON, NDJSON event streams, CLI output, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use provider API keys, outbound network access, local daemon endpoints, persistent cache, and metrics files.] <br>

## Skill Version(s): <br>
1.3.7 (source: server release metadata; package.json reports 1.3.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
