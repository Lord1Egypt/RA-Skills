## Description: <br>
Research a topic via web search, auto-match a GIF with gifgrep, and log structured notes to Bear using a customizable template. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to gather web research for a topic, select a related GIF, and create a structured Bear note from a template. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports under-disclosed persistence through Bear notes and fallback Markdown files. <br>
Mitigation: Review topics and generated note content before use, and avoid sensitive research topics unless this persistence is acceptable. <br>
Risk: The security guidance says research topics may be sent to external search and GIF tools. <br>
Mitigation: Do not use confidential topics, templates, or tags unless external disclosure is acceptable. <br>
Risk: The security guidance flags an unpinned grizzly dependency. <br>
Mitigation: Pin and review the grizzly dependency before installing in controlled environments. <br>


## Reference(s): <br>
- [Research Logger on ClawHub](https://clawhub.ai/terrycarter1985/terrycarter1985-research-logger) <br>
- [grizzly Go module](https://github.com/tylerwince/grizzly) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown note content with shell command status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a Bear note through grizzly; falls back to a Markdown file under /tmp when note creation fails.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
