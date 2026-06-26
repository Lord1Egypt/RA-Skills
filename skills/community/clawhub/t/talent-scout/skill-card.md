## Description: <br>
Scrape LinkedIn company employee pages, rank candidates with AI, and generate personalized outreach DMs and a competitive team structure brief. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Behruamm](https://clawhub.ai/user/Behruamm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Recruiting and talent intelligence users can use this skill to run a CLI workflow that gathers candidate data for a target company and role, ranks likely prospects, drafts outreach, and summarizes team structure signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs the agent to silently update and reinstall local toolkit code before use. <br>
Mitigation: Review and remove or disable the silent auto-update block; install the CLI only from a trusted, pinned source. <br>
Risk: The workflow uses recruiting data, generated outreach, and candidate profiling that may involve organizational policy, platform terms, privacy, or legal constraints. <br>
Mitigation: Confirm LinkedIn scraping, candidate profiling, generated outreach, and report retention are allowed under applicable law and internal rules before use. <br>
Risk: The skill requires external API keys for scraping and LLM providers. <br>
Mitigation: Use restricted API keys and avoid exposing secrets in prompts, reports, logs, or retained output files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and references to generated JSON and PDF report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce JSON candidate reports, outreach drafts, executive summaries, and optional PDF briefs when the CLI is run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
