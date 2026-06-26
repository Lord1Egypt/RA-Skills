## Description: <br>
Researches a topic across multiple source types and produces a cited report, with simple inline summaries or broader orchestrated research runs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanford](https://clawhub.ai/user/seanford) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to gather sources, coordinate research workers, deduplicate findings, and synthesize markdown reports for decision support, writing, or technical investigation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may spawn multiple sub-agents and contact web, search, browser, and fallback fetch services. <br>
Mitigation: Install it only where broad research automation is intended, and review runtime configuration such as sub-agent depth and timeout limits before use. <br>
Risk: Research topics, URLs, worker progress, retry queues, and reports may persist on disk. <br>
Mitigation: Treat the skills-data directory as potentially sensitive and clean ~/.openclaw/workspace/skills-data/skilled-deep-research/ after confidential research runs. <br>
Risk: Artifact behavior references hard-coded /home/sean helper-script paths for fallback fetching. <br>
Mitigation: Review or replace those helper paths with trusted local equivalents before running standard, deep, or retry workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/seanford/skilled-deep-research) <br>
- [Publisher Profile](https://clawhub.ai/user/seanford) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [DDG Search Fallback](https://github.com/seanford/ddg-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with cited sources, inline summaries, status text, and shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write checkpoint files, retry queues, metadata, and final reports under the configured OpenClaw skills-data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter states 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
