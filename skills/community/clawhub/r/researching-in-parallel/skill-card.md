## Description:

Research any topic thoroughly by running three sub-agents with distinct analytical lenses (breadth, critique, evidence), then giving their outputs to a final sub-agent to produce or update one review report with a unified bibliography.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vsamtani](https://clawhub.ai/user/vsamtani)

### License/Terms of Use:


## Use Case:

External users and researchers use this skill when they need a deep, multi-perspective research report, briefing, or synthesis rather than a quick factual lookup. It is designed for new reports and iterative updates where prior outputs can become starting-point sources for later runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spawn multiple sub-agents, run extensive web/PDF/browser research, and save generated files in the workspace.

Mitigation: Use a new empty workspace for each run, review provided-source paths before execution, and confirm the planned models and workspace before spawning sub-agents.

Risk: Generated research reports and bibliographies may contain errors, gaps, or hallucinated citations.

Mitigation: Verify generated citations and critical claims independently before relying on the report for decisions or publication.

Risk: Research quality may be reduced when browser or PDF tools are unavailable because sub-agents may be limited to snippets or abstracts.

Mitigation: Run with web, browser, and PDF retrieval available for serious research, and inspect the methodology section for access-status gaps.

## Reference(s):

- [Researching In Parallel Skill Page](https://clawhub.ai/vsamtani/skills/researching-in-parallel)
- [Configuration Reference](references/configuration.md)
- [Breadth Pass Prompt](references/prompts/breadth.md)
- [Critical Pass Prompt](references/prompts/critical.md)
- [Evidence Pass Prompt](references/prompts/evidence.md)
- [Synthesis Prompt](references/prompts/synthesis.md)
- [Updater Prompt](references/prompts/updater.md)
- [Report Template](assets/report-template.md)
- [Bibliography Template](assets/bibliography-template.md)
- [Original Parallel Research Method](https://www.bleeta.ai/post/your-30-minute-ai-research-system-a-practical-guide)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, bibliography files, prompt files, optional source extract files, and configuration-guided shell/tool actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are saved in the selected workspace and may be reused as provided sources for later research runs.]

## Skill Version(s):

1.4.2 (source: server release evidence; artifact frontmatter metadata version is 1.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
