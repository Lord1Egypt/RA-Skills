## Description: <br>
Story Short Analyze guides agents through a staged Chinese short web-fiction critique workflow that analyzes story core, structure, emotional arcs, reversals, writing techniques, characters, and reusable narrative patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[worldwonderer](https://clawhub.ai/user/worldwonderer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and agents use this skill to produce structured criticism of legally available short web fiction, including plot beats, emotional curve, hooks, reversals, craft techniques, character functions, quality checks, and reusable patterns for downstream writing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow saves the original story text and analysis files locally for later reuse. <br>
Mitigation: Use it only with works the user has the right to analyze, avoid sensitive private material, and review or remove local outputs when retention is not desired. <br>
Risk: The analysis may reflect the skill's opinionated genre framing for short web fiction. <br>
Mitigation: Review outputs before relying on them for editorial, publishing, or downstream writing decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/worldwonderer/skills/story-short-analyze) <br>
- [OpenClaw Source Metadata](https://github.com/worldwonderer/oh-story-claudecode) <br>
- [Output Contract](references/output-contract.md) <br>
- [Output Templates](references/output-templates.md) <br>
- [Short Story Decomposition Methodology](references/material-decomposition.md) <br>
- [Quality Checklist](references/quality-checklist.md) <br>
- [AI-Writing Style Checks](references/anti-ai-writing.md) <br>
- [Banned Words and Sentence Patterns](references/banned-words.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown reports plus JSON metadata written to local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local source-text backup, analysis report, plot-node report, writing-technique report, and _meta.json under 拆文库/{书名}/ unless the user specifies another path.] <br>

## Skill Version(s): <br>
1.1.7 (source: server release metadata; artifact frontmatter reports 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
