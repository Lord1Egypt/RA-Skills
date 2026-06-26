## Description: <br>
Simplified man pages from tldr-pages. Use this to quickly understand CLI tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuji10000qian-svg](https://clawhub.ai/user/liuji10000qian-svg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and command-line users use this skill to have an agent prefer concise tldr examples when explaining CLI tools, falling back to man pages or --help only when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: tldr pages are concise and may omit exact flags, edge cases, or security-sensitive details. <br>
Mitigation: For sensitive commands, exact flags, or unusual cases, verify with man pages, --help, or official documentation before acting. <br>
Risk: The skill depends on the local tldr binary and its page cache. <br>
Mitigation: Use a trusted tldr installation and update the cache in a controlled environment when command coverage appears stale or incomplete. <br>


## Reference(s): <br>
- [tldr-pages project](https://github.com/tldr-pages/tldr) <br>
- [ClawHub skill page](https://clawhub.ai/liuji10000qian-svg/tldr-20260228-xiaren) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an existing trusted tldr binary in the user's environment.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
