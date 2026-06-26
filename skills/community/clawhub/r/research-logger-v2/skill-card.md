## Description: <br>
Research a topic via web search, auto-match a related GIF, and log structured notes to Bear using a customizable template. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to turn a research topic into a structured Markdown note with source findings, optional GIF media, tags, and a Bear note entry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics are sent to Brave Search and optionally Giphy when API keys are configured. <br>
Mitigation: Avoid confidential topics unless those provider and storage behaviors are acceptable for the workspace. <br>
Risk: Generated findings and summaries may be incomplete or misleading. <br>
Mitigation: Review the generated note and source links before relying on or sharing the research output. <br>
Risk: The workflow depends on local tools and a template path that may be missing. <br>
Mitigation: Verify grizzly, curl, python3, Bear, and notes/research_template.md are available before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/research-logger-v2) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands] <br>
**Output Format:** [Markdown research note plus terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a local note file under notes/ and creates a Bear note through grizzly when that CLI is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
