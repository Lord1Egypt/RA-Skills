## Description: <br>
Automatically publishes content to Toutiao as micro-posts or articles, including AI-recommended inline images, free licensed cover images, and browser-driven publishing steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axdlee](https://clawhub.ai/user/axdlee) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Content creators, operators, and developers use this skill to prepare and publish Toutiao micro-posts or articles through browser automation. It supports title entry, rich-text content injection, image selection, declaration settings, preview, and live publishing from a logged-in Toutiao account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit live posts from a logged-in Toutiao account without a mandatory final approval gate. <br>
Mitigation: Use a dedicated browser profile or test account, review title, body, image, and declaration choices before publishing, and avoid one-shot publishing until a draft-only mode or mandatory final confirmation is available. <br>
Risk: Broad trigger phrases can cause the agent to enter a publishing workflow when the user's intent is ambiguous. <br>
Mitigation: Require explicit user confirmation before opening the publishing page or clicking preview and publish actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/axdlee/toutiao-publish) <br>
- [Publisher profile](https://clawhub.ai/user/axdlee) <br>
- [README](README.md) <br>
- [Release notes](RELEASE-NOTES.md) <br>
- [Search help](SEARCH-HELP.md) <br>
- [Toutiao creator publishing page](https://mp.toutiao.com/profile_v4/graphic/publish) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and browser automation snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute browser automation that changes account state by publishing live content.] <br>

## Skill Version(s): <br>
6.1.0 (source: SKILL.md frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
