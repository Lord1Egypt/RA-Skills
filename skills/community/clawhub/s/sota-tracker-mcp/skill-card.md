## Description: <br>
Provides daily updated model-ranking data and query tools for tracking state-of-the-art AI models across LLM, image, video, audio, embedding, and related categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romancircus](https://clawhub.ai/user/romancircus) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this release to query current AI model rankings, freshness, forbidden/outdated model lists, hardware-aware recommendations, and optional MCP or REST endpoints before selecting models for a task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated update flows can modify local agent instruction files and influence future model recommendations. <br>
Mitigation: Back up and review target agent files before enabling cron or systemd timers or running update_agents_md.py. <br>
Risk: Recommendation paths can prioritize uncensored or no-guardrail model variants when that preference is enabled. <br>
Mitigation: Keep uncensored-model preferences disabled unless those recommendations are deliberately required and approved. <br>
Risk: The tracker can update local data from external sources, so stale or changed source data may affect recommendations. <br>
Mitigation: Review refreshed data and source attribution before relying on recommendations for high-impact decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/romancircus/sota-tracker-mcp) <br>
- [LMArena leaderboard](https://lmarena.ai/leaderboard) <br>
- [Artificial Analysis](https://artificialanalysis.ai) <br>
- [Hugging Face](https://huggingface.co) <br>
- [Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, CSV, API responses, shell commands, configuration] <br>
**Output Format:** [Markdown and plain-text agent responses, JSON/CSV data exports, REST API JSON responses, and setup commands or configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may reflect scraped or cached third-party benchmark data and local hardware profile preferences.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, pyproject.toml, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
