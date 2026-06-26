## Description: <br>
Ra Lite -- Research Intelligence. Drop a topic and get an instant structured 3-source research brief. Free tier of Ra. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use Ra Lite to turn a supplied research topic into a concise, cited research brief based on three web sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The user-provided research topic may be sent through web search. <br>
Mitigation: Avoid entering confidential or sensitive topics unless the operating environment and search tools are approved for that data. <br>
Risk: A short web-sourced brief can contain incomplete, outdated, or misleading findings. <br>
Mitigation: Review cited sources and verify important claims before using the brief for decisions or publication. <br>
Risk: The setup command uses pip with --break-system-packages, which can affect system Python hygiene. <br>
Mitigation: Run installation in a virtual environment or another isolated Python environment. <br>


## Reference(s): <br>
- [Ra Lite ClawHub Page](https://clawhub.ai/occupythemilkyway/ra-lite) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown research brief with executive summary, key findings, analysis, and source links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RESEARCH_TOPIC and is designed to cite 3 authoritative, recent web sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
