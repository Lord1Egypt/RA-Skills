## Description: <br>
Wechat Mp Auto helps an agent research, draft, review, illustrate, format, and create WeChat public-account article drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wzhaojin](https://clawhub.ai/user/wzhaojin) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, content operators, and agent users use this skill to automate the workflow for WeChat public-account articles, including topic research, Markdown drafting, image selection or generation, content review, HTML formatting, and draft creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate WeChat draft creation, media upload, and account-changing helper functions beyond simple text generation. <br>
Mitigation: Install it only for a WeChat public account you are comfortable automating, use dedicated WeChat and provider credentials, and review generated content and images before public posting. <br>
Risk: Credential, token, cache, and generated media files may remain under local configuration, cache, and OpenClaw credential paths. <br>
Mitigation: Protect or clear ~/.config/wechat-mp-auto, ~/.cache/wechat-mp-auto, and relevant OpenClaw credential files on shared machines. <br>
Risk: Check-only or review-oriented runs may still involve network or media side effects. <br>
Mitigation: Avoid check-only mode for sensitive drafts unless those side effects are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wzhaojin/wechat-mp-auto) <br>
- [Project homepage](https://github.com/wzhaojin/wechat-mp-auto) <br>
- [README](README.md) <br>
- [Skill workflow](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON-like tool results, HTML strings, local file paths, media identifiers, URLs, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local cache/config files, download or generate images, upload media to WeChat, and create WeChat public-account drafts when credentials are configured.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence, metadata.json, pyproject.toml, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
