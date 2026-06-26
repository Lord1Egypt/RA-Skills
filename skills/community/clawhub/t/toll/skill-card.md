## Description: <br>
Track and display token usage statistics and estimated USD costs from Claude Code and Codex CLI sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Fullstop000](https://clawhub.ai/user/Fullstop000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Claude Code and Codex CLI token usage, cache hit rates, session counts, and estimated USD costs. It helps users choose the correct toll CLI flags and interpret the resulting metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The toll CLI reads local Claude Code and Codex CLI session history, which may expose private project names, prompts, usage details, or cost data. <br>
Mitigation: Install and run it only in trusted environments, and review JSON or CSV output before sharing it. <br>
Risk: The artifact suggests a curl-to-sh quick installer from an unpinned remote script. <br>
Mitigation: Prefer cargo install or a reviewed, pinned release when installing toll. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Fullstop000/toll) <br>
- [toll project homepage](https://github.com/Fullstop000/toll) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, JSON, CSV, Guidance] <br>
**Output Format:** [Markdown summaries with shell commands and optional CLI JSON or CSV output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include token totals, cache metrics, session counts, and estimated USD costs from local Claude Code and Codex CLI session logs.] <br>

## Skill Version(s): <br>
1.0.5 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
