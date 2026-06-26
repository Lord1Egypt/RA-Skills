## Description: <br>
Automates cross-platform posting with images to LinkedIn, X/Twitter, Facebook, WordPress, and Substack via browser automation and WordPress REST API workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quoc-modoro](https://clawhub.ai/user/quoc-modoro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators, content creators, and agents use this skill to publish prepared posts and images across social platforms, WordPress, and Substack, then verify that each destination received the intended content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can publish public content from logged-in social accounts and a configured WordPress site. <br>
Mitigation: Require the agent to show the exact text, image paths, target accounts, and destination URLs before each final post or publish action. <br>
Risk: WordPress application passwords and environment files can expose publishing access. <br>
Mitigation: Protect the WordPress env file with restrictive permissions, use a least-privilege application password, and keep revocation steps available. <br>
Risk: The workflow runs an external image overlay script before posting. <br>
Mitigation: Inspect the image script before use and verify generated files before they are uploaded or published. <br>


## Reference(s): <br>
- [ARM Upload Guide](references/arm-upload-guide.md) <br>
- [Platform Quirks & Gotchas](references/platform-quirks.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/quoc-modoro/social-auto-poster) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, browser action steps, and REST API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided post content, image paths, logged-in browser sessions, and WordPress credentials; final publish actions should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: evidence release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
