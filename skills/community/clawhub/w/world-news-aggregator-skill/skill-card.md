## Description: <br>
Aggregates global technology, stock market, AI paper, military technology, and policy news from public sources into structured intelligence-style summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bodysuperman](https://clawhub.ai/user/bodysuperman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can use this skill to gather recent public news and research links across technology, finance, AI, military technology, and policy topics, then receive concise Markdown or JSON summaries for situational awareness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script contacts third-party public news and feed sites, which can expose query topics and depend on external source availability. <br>
Mitigation: Use explicit commands for sensitive research topics and review returned links and summaries before relying on them. <br>
Risk: The helper script may install Python dependencies automatically when required packages are missing. <br>
Mitigation: Run it in a virtual environment or sandbox to avoid changing the main Python environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bodysuperman/world-news-aggregator-skill) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports or JSON records printed by a command-line helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include source names, timestamps when available, summaries, links, and feed status details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
