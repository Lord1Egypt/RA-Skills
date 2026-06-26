## Description: <br>
Automates Toutiao article publishing by generating an article from user-provided keywords, then guiding login, title and body entry, cover upload, and final publication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuxucai](https://clawhub.ai/user/liuxucai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators or agents managing a Toutiao account use this skill to draft an article from keywords, upload a cover image, and publish it through the Toutiao creator console after reviewing the content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can log into a Toutiao account and publish public content without strong consent boundaries. <br>
Mitigation: Run it only in a supervised session and require explicit final confirmation before any post is published. <br>
Risk: Account credentials and authenticated browser sessions are involved in the publishing workflow. <br>
Mitigation: Provide credentials only when needed, avoid storing them in skill files or logs, and verify the login page before entering them. <br>
Risk: Generated article text or cover prompts may be inaccurate, unsuitable, or sensitive for third-party image generation. <br>
Mitigation: Review the generated article and cover image before publishing, and avoid sending sensitive topics to third-party image generation services. <br>


## Reference(s): <br>
- [Detailed Toutiao publishing rules](references/detailed-rules.md) <br>
- [ClawHub release page](https://clawhub.ai/liuxucai/toutiao-publish-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local cover image files and issue browser automation commands during a supervised publishing session.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
