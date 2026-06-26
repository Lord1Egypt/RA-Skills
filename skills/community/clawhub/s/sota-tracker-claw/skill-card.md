## Description: <br>
Provides daily-updated rankings and metadata for state-of-the-art AI models aggregated from public benchmark and model sources via static files, local queries, REST API, or optional MCP tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romancircus](https://clawhub.ai/user/romancircus) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to query current AI model rankings, identify outdated or forbidden models, compare model options, and tailor recommendations to hardware constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated updates may repeatedly rewrite agent instruction files such as CLAUDE.md or agents.md. <br>
Mitigation: Enable cron or systemd update jobs only after reviewing the exact target path, backup behavior, and disable procedure. <br>
Risk: The REST API may expose model recommendation data if bound broadly on a network. <br>
Mitigation: Keep the API local or place it behind a firewall or trusted reverse proxy. <br>
Risk: Dependencies and scraper behavior can change over time as external sources change. <br>
Mitigation: Pin and audit dependencies, and review scraper updates before deployment. <br>
Risk: Reduced-safety or uncensored model recommendations may be surfaced. <br>
Mitigation: Filter or disable uncensored-model recommendations unless the user has explicitly approved that requirement. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/romancircus/sota-tracker-claw) <br>
- [LMArena leaderboard](https://lmarena.ai/leaderboard) <br>
- [Artificial Analysis](https://artificialanalysis.ai) <br>
- [Hugging Face](https://huggingface.co) <br>
- [Civitai](https://civitai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text with JSON, CSV, SQLite, REST API, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce model recommendations, freshness checks, comparison summaries, API responses, local query examples, and agent instruction-file update guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
