## Description: <br>
技能免费版 is a basic AI agent skill vetting tool that guides source checks and RED FLAGS code review before installing other skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to perform a quick manual safety screen of another skill before installation, including source checks, RED FLAGS review, and a basic install recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat generic API_KEY and callback_url references as required setup and provide secrets unnecessarily. <br>
Mitigation: Treat those fields as generic template placeholders and avoid providing secrets unless a concrete trusted workflow requires them. <br>
Risk: The skill provides manual checklist guidance, so source checks and RED FLAGS review can be incomplete if the user skips files or metadata. <br>
Mitigation: Read all files in the target skill, verify source and publisher details, and use the report as an installation aid rather than a substitute for review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/skill-vetter-free) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown or structured JSON-style review report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a basic vetting report with RED FLAGS and SAFE TO INSTALL / DO NOT INSTALL guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
