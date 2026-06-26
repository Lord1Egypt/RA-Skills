## Description: <br>
Visual Benchmarker guides an agent to extract project search keywords, call a Douyin video search skill, and return visual benchmark video cases for confirming visual and editing style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahsbnb](https://clawhub.ai/user/ahsbnb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, creative, and content strategy agents use this skill to turn project materials into search keywords, find Douyin reference videos through a dependent search skill, and produce a concise visual benchmarking report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on a separate douyin-video-search skill and that dependency's TikHub API token configuration. <br>
Mitigation: Review and configure the dependency before use, and confirm the external search service is acceptable for the project context. <br>
Risk: Search keywords may reveal confidential strategy, product, or campaign details to an external search service. <br>
Mitigation: Use only keywords that are safe to disclose, and summarize or generalize sensitive project details before searching. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ahsbnb/visual-benchmarker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with recommended benchmark videos, links, visual analysis, and reusable creative notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a separate douyin-video-search skill and may pass extracted search keywords to that dependency.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
