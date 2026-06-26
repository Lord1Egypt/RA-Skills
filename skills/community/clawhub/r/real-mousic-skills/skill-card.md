## Description: <br>
Searches gequhai.com for songs and returns third-party download links when a user asks to search for or download music. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[xiaoyiyebuaijianghua](https://clawhub.ai/user/xiaoyiyebuaijianghua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents use this skill to search a third-party music-link site for requested songs, present candidate matches, and return download-link options after the user selects a result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an automated Chrome profile with stealth and fingerprint-masking behavior. <br>
Mitigation: Use an isolated Chrome profile and debug port, and avoid logging into unrelated accounts in that browser profile. <br>
Risk: The skill may close or kill a process on the configured Chrome debug port. <br>
Mitigation: Run it on a dedicated port and review active processes before execution. <br>
Risk: Returned music links come from third-party sites and may create safety or copyright concerns. <br>
Mitigation: Verify link safety and copyright authorization before opening or downloading any linked content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoyiyebuaijianghua/real-mousic-skills) <br>
- [gequhai.com](https://www.gequhai.com/) <br>
- [Quark Drive](https://pan.quark.cn/) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>
- [OpenClaw](https://github.com/anthropics/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with search results, download-link options, warnings, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI returns JSON that the agent formats for the user; direct links should include safety and copyright cautions.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter and pyproject.toml show 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
