## Description: <br>
Publishes new posts and edits existing posts in a Typecho blog through the browser-based Typecho admin workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ljzxzxl](https://clawhub.ai/user/ljzxzxl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Blog owners and operators use this skill to create, edit, categorize, and publish Typecho blog posts with an agent controlling a browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or update real Typecho blog content using stored credentials without clear pre-publish confirmation safeguards. <br>
Mitigation: Require the agent to show the target blog, title, content summary, category, and create-or-edit action before any publish or save action. <br>
Risk: Over-scoped Typecho credentials could grant broader access than needed for routine publishing. <br>
Mitigation: Use a dedicated low-privilege Typecho account where possible and avoid storing a full administrator password. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ljzxzxl/typecho-post-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions and browser-operation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or edit public blog content when used with browser control and configured Typecho credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
