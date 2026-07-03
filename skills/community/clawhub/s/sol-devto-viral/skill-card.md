## Description: <br>
Dev.to viral engine that mines trending AI stories, prepares contextual promotion copy for Sol's posts, and cross-posts new blog content to dev.to. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amrree](https://clawhub.ai/user/amrree) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to research trending dev.to AI articles, prepare contextual comment copy, and cross-post Jekyll blog posts to dev.to. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled automation can access a local blog repository, API credentials, and public dev.to posting flows without enough scoping or user control. <br>
Mitigation: Review before installing, grant only the intended repository and credential access, require dry-run behavior, and require explicit approval before publishing to dev.to. <br>
Risk: Embedded or locally stored API keys may expose dev.to or MiniMax credentials. <br>
Mitigation: Move embedded API keys to a safer secret store or environment variable and rotate any credential that may have been exposed. <br>
Risk: The referenced external devto-viral.py script controls important behavior that is not included in the artifact. <br>
Mitigation: Verify the external script before use and scan it with the same security expectations as the skill manifest. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amrree/skills/sol-devto-viral) <br>
- [Referenced sol-skills-bundle source](https://github.com/TheSolAI/sol-skills-bundle) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [Markdown content, contextual text, and JSON log records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes trend, advertisement, and cross-post tracking logs; may publish adapted posts through the dev.to API.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
