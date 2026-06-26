## Description: <br>
Publish posts to Weibo (Sina Weibo) using browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azfliao](https://clawhub.ai/user/azfliao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to draft, publish, schedule, and verify Weibo posts from a logged-in browser session. It is suited for text posts that may include emoji, hashtags, mentions, line breaks, and Chinese content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish public Weibo posts from a logged-in browser session. <br>
Mitigation: Require explicit user confirmation before each live or scheduled post and use only an account and browser profile approved for automation. <br>
Risk: Unattended or recurring posting examples could publish content without timely human review. <br>
Mitigation: Avoid hourly or trending-news automation patterns unless a human approval gate is added before publication. <br>
Risk: Post content may be stored in a local state file after successful publication. <br>
Mitigation: Clear, restrict, or avoid the local state file when post content is sensitive. <br>
Risk: Moderation-evasion guidance appears in the reviewed material. <br>
Mitigation: Do not follow sensitive-word evasion advice; revise content to comply with applicable platform rules and review requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/azfliao/weibo-publisher) <br>
- [Weibo Publishing Examples](references/EXAMPLES.md) <br>
- [Weibo Publishing Troubleshooting](references/TROUBLESHOOTING.md) <br>
- [Unicode Escape Guide](references/UNICODE_ESCAPE.md) <br>
- [Quick Reference](QUICK_REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with inline browser automation calls, Python snippets, JSON state examples, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces posting workflows and verification steps; optional helper script can update local posting state.] <br>

## Skill Version(s): <br>
2.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
